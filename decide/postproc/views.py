from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
import math
#import numpy as np


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

    def HuntingtonHill(self,numEscanos,options):
    
        votosTotales = 0
        for x in options:
            votosTotales += x['votes']
        
        if votosTotales > 0 and numEscanos > 0:

            limite = votosTotales/numEscanos

            #Crear parametros para metodo rounding rule
            rounding = limite*0.001
            lower = limite-rounding
            upper = limite+rounding

            numEscanosAsig = 0

            while(numEscanosAsig != numEscanos):

                #si llegamos a aplicar rounding rule y no llegamos al numero igual de escanos, 
                #reseteamos de nuevo el numero de escanos asig y empezamos de nuevo
                numEscanosAsig = 0

                for x in options:

                    if(x['votes']<limite):
                        x['postproc']=0
                    else:
                        cuota = x['votes']/limite
                        
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
                
                    numEscanosAsig += x['postproc']

                #Huntington-Hill Rounding Rule
                #For a quota q, let L denote its lower quota, U its upper quota, and G the
                #geometric mean of L and U. If then round q down to L, otherwise
                #round q up to U.

                if(numEscanosAsig < numEscanos):
                    limite = lower
                    lower = limite-rounding
                    upper = limite+rounding

                else:
                    limite = upper
                    lower = limite-rounding
                    upper = limite+rounding
        else:
            for x in options:
                x.update({'postproc' : 0})
            return Response(options)
        
        return Response(options)


    def imperiali(self, options,numEscanyos):
        votosTotales = 0
        
        for i in options:
            votosTotales= votosTotales+ i['votes']
        
        if votosTotales>0 and numEscanyos>0:

            q=round(votosTotales/(numEscanyos+2),0)

            escanyosAsigandos=0
            for i in options:
                votos= i['votes']
                escanyos=math.floor(votos/q)
                i.update({'postproc': escanyos})
                escanyosAsigandos=escanyosAsigandos+i['postproc']
            
            #Mientras queden escaños libre

            while(escanyosAsigandos<numEscanyos):
                #Se almacenan los votos residuo
                for i in options:
                    i.update({'votosResiduos': i['votes']- (q*i['postproc'])})
                
                
                #se ordena según los votos residuos
                ordenadoMayorMenor= options.sort(key = lambda i :-i['votosResiduos'])


                #se añade un escaño más al que tenga mayor residuo
                votoMayorResiduo= ordenadoMayorMenor[0]
                votoMayorResiduo.update({'postproc': votoMayorResiduo['postproc']+1})

                #se elimina la nueva clave para que no afecte a futuras iteraciones
                for i in options:
                    i.pop('votosResiduos')
                
            options.sort(key = lambda i :-i['postproc'])

            return Response(options)
            
        else:
            for i in options:
                i.update({'postproc': 0})
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
        numEscanos = request.data.get('numEscanyos', 0)

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t=='IMPERIALI':
            return self.imperiali(opts,numEscanos)
 
            
        return Response({})
