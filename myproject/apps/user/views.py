from django.http import HttpResponse
from django.shortcuts import render
from user import models


# Create your views here.

def one_to_one(request):
    # 子表查询母表,找到红球对应的颜色#写法1：
    print(models.Ball.objects.get(
        description="红球").color.colors)  # 返回红，通过子表查询母表，写法："子表对象.母表表名的小写.母表字段名" ；通过Ball表查到description为"红球"，查找到对应colors
    # 写法2，反向从母表入手：
    print(models.Colors.objects.get(
        ball__description="红球").colors)  # 返回红，通过子表查询母表，但形式上是从母表对象自身直接获取字段，写法："母表.objects.get(
    # 子表名小写__子表字段="xxx").母表字段名" ；效果和上边完全一致，另一种形式

    # 母表查询子表，找到红色对应的球的名字#写法1：print(models.Colors.objects.get(colors="红").ball.description)
    # #返回红球，通过母表查询子表，写法："母表对象.子表表名的小写.子表字段名"；找到颜色为红色的Ball的description 写法2，反向从子表入手：
    print(models.Ball.objects.get(
        color__colors="红").description)  # 返回红球，通过母表查询子表，但形式上是从子表对象自身直接获取字段，写法："子表.objects.get(
    # 一对一的子表字段__母表字段="xxx").子表字段"；效果和上边完全一致，另一种形式

    # 增添数据的三种写法：
    # 写法1：
    color_obj = models.Colors.objects.create(colors="黑")
    models.Ball.objects.create(color=color_obj, description="黑球")
    # 写法1补充：
    color_id = models.Colors.objects.create(colors="黑").id
    models.Ball.objects.create(color_id=color_id, description="黑球")
    # 写法2：
    color_obj = models.Colors.objects.create(colors="黑")
    ball_obj = models.Ball(color=color_obj, description="黑球")
    ball_obj.save()
    # 写法3(字典导入)：
    color_obj = models.Colors.objects.create(colors="黑")
    ball_dic = {'description': "黑球"}
    models.Ball.objects.create(color=color_obj, **ball_dic)

    # 更新一条数据
    color_obj = models.Colors.objects.get(colors="黑")
    color_obj.colors = "灰"
    color_obj.save()
    # 更新多条数据，把满足条件的球的description都变为灰球
    # 写法1：
    models.Ball.objects.filter(color__colors="红").update(description="灰球")
    # 写法2：
    up_dic = {"description": "灰球"}
    models.Ball.objects.filter(id__gt=0).update(**up_dic)

    # 删
    models.Ball.objects.get(description="灰球").delete()  # 对象和QuerySet都有方法delete()
    models.Colors.objects.filter(colors="灰").delete()

    models.Colors.objects.all().delete()  # 清空一张表

    return HttpResponse("success!")


def one_to_money(request):
    # 外键表联合查询：

    # 外键子表查询母表,与一对一子表查询母表形式一致
    # 找到红裤衩所属的颜色表中的颜色--返回:红
    # 写法1：
    print(models.Clothes.objects.get(
        description="小虎哥").color.colors)  # 返回红，通过子表查询母表，写法："子表对象.母表表名的小写.母表字段名"
    # ；通过Clothes表查到description为"小虎哥"，查找到对应colors
    # 写法2，反向从母表入手：
    print(models.Colors.objects.get(
        clothes__description="小虎哥").colors)  # 返回红，通过子表查询母表，但形式上是从母表对象自身直接获取字段，写法："母表.objects.get(
    # 子表名小写__子表字段="xxx").母表字段名" ；效果和上边完全一致，另一种形式

    # 外键母表查询子表,与一对一形式不同，因为母表为"多"，不能像一对一一样通过.get().子表.子表字段的方式获取，但与多对多母表查询子表一致
    # 找到颜色为红的所有服装--返回:[<Clothes: 大美女>, <Clothes: 小虎哥>]
    # 写法1：
    color_obj = models.Colors.objects.get(colors="红")
    print(color_obj.clothes_set.all())  # 注意：子表小写_set的写法,它实际上是一个QuerySet,可以用update,delete,all,filter等方法
    # 写法2：
    print(models.Clothes.objects.filter(color=models.Colors.objects.get(colors="红")))
    # 写法2简便写法（推荐）：
    print(models.Clothes.objects.filter(color__colors="红"))  # 写法：filter(子表外键字段__母表字段='过滤条件')#写法3：
    color_id = models.Colors.objects.get(colors="红").id  # 通过母表获取到颜色为红的id
    print(models.Clothes.objects.filter(color_id=color_id))  # filter得到QuerySet,写法：filter(子表外键字段_母表主键=母表主键对象)

    print(models.Clothes.objects.filter(color=models.Colors.objects.get(colors="红")).values('color__colors',
                                                                                            'description'))  # 获取子表的description字段，和母表的colors字段，获取母表字段写法: 子表外键字段名__母表字段名--适用于values()或filter()
    # 简写形式补充：
    print(models.Clothes.objects.filter(color__colors="红").values('color__colors', 'description'))
    # 返回：
    # [{'description': u'\u7ea2\u5185\u8863', 'color__colors': u'\u7ea2'},
    #  {'description': u'\u7ea2\u5185\u88e4', 'color__colors': u'\u7ea2'}]
    # 如果不加values(),返回的是[<Clothes: 大美女>, <Clothes: 小虎哥>]这样一个QuerySet集合，通过values可以形成一个列表，列表中的每一个元素是一个字典，可以通过list()将ValuesQeurySet转化为列表，之后返回给templates

    # 另外可通过.values_list()将QuerySet转化为ValuesListQuerySet。返回：[(u'\u7ea2', u'\u7ea2\u889c\u5b50'), (u'\u7ea2', u'\u7ea2\u889c\u5b50')]
    # 得到的是一个列表，列表中是多个元组，每个元组是ValuesQuerySet中字典的value，常用于从models里将数据取出后动态添加到前端模板中的select选项中。
    # 通过forms.py从models取值传给前端select选项，需重启django后，select选项才能更新，可在定义form时，添加如下关键字保障动态更新select选项
    # forms.py
    from django import forms
    class ClothesForm(forms.Form):
        color = forms.IntegerField(required=True, widget=forms.Select(), )

        def __init__(self, *args, **kwargs):  # 定义这个关键字段，当使用form时，colors表新增了颜色，前端ClothesForm的color字段的选项会自动更新
            super(ClothesForm, self).__init__(*args, **kwargs)
            self.fields['color'].widget.choices = models.Colors.objects.all().order_by('id').values_list('id', 'colors')

    # 增添子表数据，形式与一对一一致
    # 添加颜色为绿的服装：小帅哥
    # 方法1：
    models.Clothes.objects.create(color=models.Colors.objects.get(colors="绿"), description="小帅哥")
    # 方法1补充：
    models.Clothes.objects.create(color_id=models.Colors.objects.get(colors="绿").id, description="小帅哥")
    # 方法2：
    c_obj = models.Clothes(color=models.Colors.objects.get(colors="绿"), description="小帅哥")
    c_obj.save()
    # 方法3：字典方式录入..参考一对一

    # 颜色为红的服装，description都更新为大美女
    # 写法1：
    models.Clothes.objects.filter(color__colors="红").update(description="大美女")
    # 写法2：
    models.Clothes.objects.filter(color_id=models.Colors.objects.get(colors="红").id).update(description="大美女")
    # 写法3：
    colors_obj = models.Colors.objects.get(colors="红")
    colors_obj.clothes_set.filter(id__gte=1).update(description="大美女")
    # 其他写法参照一对一的修改和外键的查询

    models.Clothes.objects.get(description="灰裙子").delete()  # 对象和QuerySet都有方法delete()
    models.Colors.objects.filter(colors="灰").delete()


def money_to_money(request):
    # 多对多子表查询母表,查找小明喜欢哪些颜色--返回:[<Colors: 红>, <Colors: 黄>, <Colors: 蓝>]
    # 与一对多子表查询母表的形式不同，因为一对多，查询的是母表的“一”；多对多，查询的是母表的“多”
    # 写法1：
    child_obj = models.Child.objects.get(name="小明")  # 写法：子表对象.子表多对多字段.过滤条件(all()/filter())
    print(child_obj.favor.all())
    # 写法2，反向从母表入手：
    print(models.Colors.objects.filter(child__name="小明"))  # 母表对象.filter(子表表名小写__子表字段名="过滤条件")

    # 多对多母表查询子表,查找有哪些人喜欢黄色--返回:[<Child: 小明>, <Child: 丫蛋>]
    # 与一对多母表查询子表的形式完全一致，因为查到的都是QuerySet，一对多和多对多，都是在查询子表的“多”
    # 写法1：
    color_obj = models.Colors.objects.get(colors="黄")
    print(color_obj.child_set.all())
    # 写法2：
    print(models.Child.objects.filter(favor=models.Colors.objects.get(colors="黄")))
    # 写法2简便写法(推荐):
    print(models.Child.objects.filter(favor__colors="黄"))  # 写法：filter(子表外键字段__母表字段='过滤条件')
    # 写法3：
    color_id = models.Colors.objects.get(colors="黄").id  # 通过母表获取到颜色为红的id
    print(models.Child.objects.filter(
        favor=color_id))  # filter得到QuerySet,写法：filter(子表外键字段=母表主键对象),此处和一对多略有不同，是子表外键字段而不是外键字段_母表主键

    # 添加子表关联关系
    # 添加小虎并让他喜欢所有颜色
    # 写法1：
    child_obj = models.Child.objects.create(name="小虎")  # 如果是已有用户，使用.get()
    colors_obj = models.Colors.objects.all()  # 创建颜色表的所有颜色QuerySet对象
    child_obj.favor.add(*colors_obj)  # 添加对应关系,将小虎和所有颜色进行关联，写法：子表对象.子表多对多字段.add(*QuerySet对象)
    # 写法2：
    child_obj = models.Child.objects.get(name="小虎")
    colors_obj = models.Colors.objects.all()
    child_obj.favor = colors_obj
    child_obj.save()
    # 让小虎喜欢黄色和蓝色(2种写法和上边一致，只展示一种写法)
    child_obj = models.Child.objects.get(name="小虎")
    colors_obj = models.Colors.objects.filter(colors__in=["蓝", "黄"])  # models默认只能用这种方式得到并集，如需更复杂的过滤逻辑，需使用模块Q
    child_obj.favor.clear()  # 清空小虎已经喜欢的颜色
    child_obj.favor.add(*colors_obj)  # add是追加模式，如果当前小虎已经喜欢绿色，那么执行后，小虎会额外喜欢蓝，黄
    # 让小虎喜欢绿色(2种写法和上边一致，只展示一种写法)
    child_obj = models.Child.objects.get(name="小虎")
    colors_obj = models.Colors.objects.get(colors="绿")
    child_obj.favor.clear()
    child_obj.favor.add(colors_obj)  # 此处没有*#添加母表关联关系
    # 让喜欢蓝色的人里添加小虎,可以用上边的方法，一个效果，让小虎喜欢蓝色，下边介绍反向插入(从母表入手)的写法
    child_obj = models.Child.objects.get(name="小虎")
    colors_obj = models.Colors.objects.get(colors="蓝")
    colors_obj.child_set.add(child_obj)  # 从colors表插入小虎，写法：母表对象.子表名小写_set.add(子表对象)。 让喜欢蓝色的child_set集合添加name="小虎"
    # 让所有人都喜欢蓝色
    children_obj = models.Child.objects.all()
    colors_obj = models.Colors.objects.get(colors="蓝")
    colors_obj.child_set.add(*children_obj)
    # 关于_set写法，是否已经有些晕了，究竟什么时候使用_set,简单记忆，只有子表才有"子表名小写_set"的写法，得到的是一个QuerySet集合，后边可以接.add(),.remove(),.update(),.delete(),.clear()
    # 另外备注一下，colors_obj.child_set.clear()是让所有人喜欢的颜色里去掉蓝色，colors_obj.child_set.all().delete()是删除.child_set的所有人

    # 删除子表与母表关联关系
    # 让小虎不喜欢任何颜色
    # 写法1：
    child_obj = models.Child.objects.get(name="小虎")
    colors_obj = models.Colors.objects.all()
    child_obj.favor = ''
    child_obj.save()
    # 写法2：
    child_obj = models.Child.objects.get(name="小虎")
    colors_obj = models.Colors.objects.all()
    child_obj.favor.remove(*colors_obj)
    # 写法3：
    child_obj = models.Child.objects.get(name="小虎")
    child_obj.favor.clear()
    # 其他例子参照多对多的增与改案例，这里不做举例

    # 删除母表与子表关联关系
    # 让所有人不再喜欢蓝色
    # 写法1：
    children_obj = models.Child.objects.all()
    colors_obj = models.Colors.objects.get(colors="蓝")
    colors_obj.child_set.remove(*children_obj)
    # 写法2：
    colors_obj = models.Colors.objects.get(colors="蓝")
    colors_obj.child_set.clear()

    # 删除子表数据
    # 喜欢蓝色的所有人都删掉
    colors_obj = models.Colors.objects.get(colors="蓝")
    colors_obj.child_set.all().delete()  # 注意有.all()
    # 删除所有child
    models.Child.objects.all().delete()
