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


    def dHont(self, options, numEscanyos):

        #Añadimos un campo para el contador de escaños asignados a cada opción
        for op in options:
            op['postproc'] = 0
        
        #Para cada escaño recorremos todas las opciones usando la fórmula de d'Hont: número de votos de esa opción/(número de escaños asignados a esa opción + 1)
        for escano in range(0, numEscanyos):
             #Lista de tamaño igual al número de opciones. Recuento al aplicar la fórmula a cada opción (ordenados en la misma forma)
            recuento = []
            for op in options:
                r = op['votes'] / (op['postproc']+1)
                recuento.append(r)
            
            #Obtenemos el índice del máximo valor en la lista de recuento de votos (del ganador del escaño)
            ganador = recuento.index(max(recuento))
            #En la posicion del ganador le sumamos 1 escaño
            options[ganador]['postproc'] += 1

        return Response(options)


    def post(self, request):
        """
         * type: IDENTITY | HUNTINGTONHILL | DHONT
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

        elif t == 'DHONT':
            return self.dHont(options=opts, numEscanyos=numEscanyos)

        return Response({})
