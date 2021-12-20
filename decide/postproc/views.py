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


    def bipartitanship(self, options, numEscanyos):
        def sortByVotes(e):
            return e['votes']
        opts = options
        opts.sort(reverse=True,key=sortByVotes)
        option1=opts[0]
        option2=opts[1]
        votosTotales = option1['votes'] + option2['votes']
        proporcion = numEscanyos/votosTotales
        escanyos1 = round(option1['votes']*proporcion)
        escanyos2 = round(option2['votes']*proporcion)
        sumaEscanyos = escanyos1 + escanyos2
        if sumaEscanyos != numEscanyos:
            sobrante = numEscanyos-sumaEscanyos
            escanyos1 +=sobrante
        for op in opts:
            op['postproc'] = 0
        opts[0]['postproc'] = escanyos1
        opts[1]['postproc'] = escanyos2
        options = opts
        return Response(options)


    def post(self, request):
        """
         * type: IDENTITY | BIPARTITANSHIP
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

        elif t == 'BIPARTISHANSHIP':
            return self.bipartishanship(options=opts, numEscanyos=numEscanyos)

        return Response({})