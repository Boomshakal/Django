from pymssql import ProgrammingError
from pymssql import OperationalError
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.database.database_connect import DatabasePool
# from django.db import connection


# Create your views here.
from utils.exceptions import CommonException
from utils.response import BaseResponse


class JihuaView(APIView):
    def get(self, request):
        response = BaseResponse()
        sql = '''
            exec p_mm_wo_workshop_plan_get_items_finereport_dv
    
            '''
        p = ()
        try:
            connect = DatabasePool('core_erp')
            lists = connect.ExecQuery(sql, p)

            response.code = 1000
            response.msg = '获取计划数据'
            response.data = lists

        except ProgrammingError as e:
            response.code = e.args[0]
            response.error = e.args[1]

        except OperationalError as e:
            response.code = e.args[0]
            response.error = e.args[1]

        # for i in lists:
        #     print(i)

        return Response(response.dict)


class ProdectView(APIView):
    def get(self, request):
        work_line = request.query_params.get('work_line')
        # print(work_line)
        sql = '''
        exec p_fm_get_work_board_and %s
        '''
        p = (work_line,)

        response = BaseResponse()
        try:
            connect = DatabasePool('core_win')
            lists = connect.ExecQuery(sql, p)
            response.code = 1000
            response.msg = '获取计划数据'
            response.data = lists

        except ProgrammingError as e:
            response.code = e.args[0]
            response.error = e.args[1]

        except OperationalError as e:
            response.code = e.args[0]
            response.error = e.args[1]

        return Response(response.dict)


class LineInfoView(APIView):
    def get(self, request):
        work_line = request.query_params.get('work_line')
        print(request.data)
        sql = '''
        select * from fm_work_line where code = %s
        '''
        p = (work_line,)

        response = BaseResponse()
        try:
            connect = DatabasePool('core_win')
            lists = connect.ExecQuery(sql, p)

            response.code = 1000
            response.msg = '获取产线数据'
            response.data = lists

        except ProgrammingError as e:
            response.code = e.args[0]
            response.error = e.args[1]

        except OperationalError as e:
            response.code = e.args[0]
            response.error = e.args[1]

        return Response(response.dict)
