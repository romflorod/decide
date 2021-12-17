from rest_framework.views import APIView
from rest_framework.response import Response


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

    def hamilton(self, options, numEscanos):
        #Definimos votos totales y el numero de escanyos asignados
        votos = 0
        numEscanosAsignados=0
        #Hacemos recuento de votos totales y le añadimos a cada opción otro valor llamado postproc en el que almacenaremos el numero de escanyos que le asignamos
        for option in options:
            option['postproc']=0
            votos += option['votes']
        #Creamos una lista vacia para introducir el resto de cada partido al anyadir los escanyos
        lista=[]
        if votos>0 and numEscanos>0:
            participantes = len(options)
            #Recorremos las opciones y al atributo postproc que habiamos creado anteriormente le asignamos un numero de escanyos mediante 
            #el siguiente calculo: (NumVotosPartido*NumEscanyos)//VotosTotales. El resultado sera una division exacta
            #A su vez rellenamos la lista vacia con un diccionario en el que ponemos el nombre de la opcion y el resto de la division
            #Tambien vamos incrementando el numero de escanyos asignados
            for option in options:
                option['postproc']=(option['votes']*numEscanos)//votos
                lista.append({'number':option['number'],'votes':(option['votes']*numEscanos)%votos})
                numEscanosAsignados+=(option['votes']*numEscanos)//votos


            lista.sort(key=lambda o: o['votes'],reverse=True)
            for option in lista:
                i = option['number']-1
                if(numEscanosAsignados<numEscanos):
                    options[i].update({'postproc' : options[i]['postproc']+1})
                    numEscanosAsignados+=1
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

        if t == 'IDENTITY':
            return self.identity(opts)

        return Response({})
