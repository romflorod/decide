from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
import math
import numpy as np


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def HuntingtonHill(self,options,numEscanyos):
    
        votosTotales = 0
        for x in options:
            votosTotales += x['votes']
        
        if votosTotales > 0 and numEscanyos > 0:

            limit = votosTotales/numEscanyos

            #Vamos a aplicar la regla rounding
            rounding = limit*0.001
            lower = limit-rounding
            upper = limit+rounding

            numEscanyosAsig = 0

            while(numEscanyosAsig != numEscanyos):

              ##si no se cumple la regla reseteamos  cero
                numEscanyosAsig = 0

                for x in options:

                    if(x['votes']<limit):
                        x['postproc']=0
                    else:
                        cuota = x['votes']/limit
                        
                        if(isinstance(cuota,int)):
                            x['postproc']=cuota
                        else:
                            #Calculamos las cotas superior e inferior de la cuota y despues la media geometrica
                            lQ = int(cuota)
                            mediaG = math.sqrt(lQ*(lQ+1))

                            if(cuota > mediaG):
                                x['postproc']=(lQ+1)
                            else:
                                x['postproc']=lQ
                
                    numEscanyosAsig += x['postproc']

                #Rounding Rule:
                
                
                #For a quota q, let L denote it's lower quota, U its upper quota, and G the
                #geometric mean of L and U. If then round q down to L, otherwise
                #round q up to U.

                if(numEscanyosAsig < numEscanyos):
                    limit = lower
                    lower = limit-rounding
                    upper = limit+rounding

                else:
                    limit = upper
                    lower = limit-rounding
                    upper = limit+rounding
        else:
            for x in options:
                x.update({'postproc' : 0})
            return Response(options)
        
        return Response(options)


    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])
        numEscanyos = request.data.get('numEscanyos', 0)


        if t == 'IDENTITY':
            return self.identity(opts)
        elif t=='HUNTINGTONHILL':
            return self.HuntingtonHill(options=opts, numEscanyos=numEscanyos)
            

        return Response({})
