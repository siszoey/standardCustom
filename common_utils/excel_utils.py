# -*- coding: utf-8 -*-
import xlwt
import sys
import StringIO
from django.http import HttpResponse
reload(sys)
sys.setdefaultencoding('utf8')


def export_excel(request,filename,titles,datas):  
    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')  
    response['Content-Disposition'] = 'attachment;filename='+filename+'.xls'  
    # new一个文件
    wb = xlwt.Workbook(encoding = 'utf-8')  
    # new一个sheet
    sheet = wb.add_sheet(filename)
    # 维护一些样式， style_heading, style_body, style_red, style_green
    style_heading = xlwt.easyxf("""
        font:
            name Arial,
            colour_index white,
            bold on,
            height 0xA0;
        align:
            wrap off,
            vert center,
            horiz center;
        pattern:
            pattern solid,
            fore-colour 0x19;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """
    )
    style_body = xlwt.easyxf("""
        font:
            name Arial,
            bold off,
            height 0XA0;
        align:
            wrap on,
            vert center,
            horiz left;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """
    )
    style_green = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x11;")
    style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")
    fmts = [
        'M/D/YY',
        'D-MMM-YY',
        'D-MMM',
        'MMM-YY',
        'h:mm AM/PM',
        'h:mm:ss AM/PM',
        'h:mm',
        'h:mm:ss',
        'M/D/YY h:mm',
        'mm:ss',
        '[h]:mm:ss',
        'mm:ss.0',
    ]
    style_body.num_format_str = fmts[0]

    # 写标题栏
    i = 0
    for title in titles:
        sheet.write(0,i, title['name'], style_heading)
        i = i+1
    # 写数据
    row = 1
    for item in datas:
        j = 0
        for title in titles:
            sheet.write(row,j, item[title['code']], style_body)
            j = j + 1
        row = row + 1  
    
    # 写出到IO
    output = StringIO.StringIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())  
    return response