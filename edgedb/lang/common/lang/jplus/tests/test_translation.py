##
# Copyright (c) 2012 Sprymix Inc.
# All rights reserved.
#
# See LICENSE for details.
##


from . import base as base_test


class TestTranslation(base_test.BaseJPlusTest):
    def test_utils_lang_jp_tr_empty(self):
        '''JS+
        '''

    def test_utils_lang_jp_tr_almost_empty(self):
        '''JS+
        print(1);

        %%
        1
        '''

    def test_utils_lang_jp_tr_scope_1(self):
        '''JS+
        a = 2;
        function aaa() {
            a = 3;
        }
        aaa();
        print(a);

        %%
        2
        '''

    def test_utils_lang_jp_tr_scope_2(self):
        '''JS+
        a = 2;
        function aaa() {
            nonlocal a;
            a = 3;
        }
        aaa();
        print(a);

        %%
        3
        '''

    def test_utils_lang_jp_tr_scope_3(self):
        '''JS+
        a = 2;
        function aaa(a) {
            a = 3;
        }
        aaa();
        print(a);

        %%
        2
        '''

    def test_utils_lang_jp_tr_class_1(self):
        '''JS+

        class Foo {
            function bar() {
                return 10;
            }
        }

        print(Foo().bar())

        %%
        10
        '''

    def test_utils_lang_jp_tr_class_2(self):
        '''JS+

        class Foo {
            x = 10;

            function bar(a, b) {
                return this.x + (a || 0) + (b || 0);
            }
        }

        class Bar {}

        class Spam(Foo, Bar) {
            function bar() {
                return super().bar(1, 2) + 29;
            }
        }

        print(Spam().bar() + new Spam().bar())

        %%
        84
        '''

    def test_utils_lang_jp_tr_class_3(self):
        '''JS+

        class Foo {
            static x = 10;

            static function bar(a, b) {
                return this.x + (a || 0) + (b || 0);
            }
        }

        class Bar {}

        class Spam(Foo, Bar) {
            static function bar() {
                return super().bar(1, 2) + 29;
            }
        }

        print(Spam.bar())

        %%
        42
        '''

    def test_utils_lang_jp_tr_metaclass_1(self):
        '''JS+

        class MA(type) {
            static function construct(name, bases, dct) {
                dct.foo = name + name;
                return super().construct(name, bases, dct)
            }
        }

        class A(metaclass=MA) {}

        class B(A, object) {}

        print(A().foo + ' | ' + B().foo)

        %%
        __main__.A__main__.A | __main__.B__main__.B
        '''

    def test_utils_lang_jp_tr_class_super_1(self):
        '''JS+

        class Foo {
            function construct(base) {
                this.base = base;
            }

            function ham(b) {
                return this.base + b;
            }
        }

        class Bar(Foo) {
            function ham(b) {
                return super().ham.apply(this, arguments) + 100;
            }
        }

        class Baz(Bar) {
            function ham(base, b) {
                meth = super().ham;
                if (base) {
                    return meth.call(base, b);
                } else {
                    return meth.call(this, b);
                }
            }

        }

        baz = Baz(10)
        baz2 = Baz(20000)
        print(baz.ham(null, 10) + '|' + baz.ham(baz2, 10))

        %%
        120|20110
        '''

    def test_utils_lang_jp_tr_dec_1(self):
        '''JS+

        function make_dec(inc, sign) {
            return function dec(func) {
                return function() {
                    if (!sign) {
                        return func.apply(this, arguments) + inc;
                    } else {
                        return func.apply(this, arguments) * inc;
                    }
                }
            }
        }

        dec1 = make_dec(10, '+');

        @dec1
        @make_dec(20, '*')
        function abc() {
            return 20;
        }

        print(abc());

        %%
        4000
        '''

    def test_utils_lang_jp_tr_dec_n_classes_1(self):
        '''JS+

        function dec(func) {
            return function() {
                return func.apply(this, arguments) + 10;
            }
        }

        function class_dec(cls) {
            cls.attr = -11;
            return cls;
        }

        @class_dec
        class Foo {
            @dec
            function spam() {
                return 11;
            }

            @dec
            static function ham() {
                return 22;
            }
        }

        print(Foo().spam() + Foo.ham() + Foo.attr)

        %%
        42
        '''

    def test_utils_lang_jp_tr_dec_n_classes_2(self):
        '''JS+

        function one_dec(obj) {
            return 1;
        }

        @one_dec
        class Foo {}

        class Bar {
            @one_dec
            static function abc() {
                return 10;
            }

            @one_dec
            @one_dec
            static function edf() {
                return 10;
            }
        }

        print(Foo + Bar.abc + Bar.edf)

        %%
        3
        '''

    def test_utils_lang_jp_tr_func_defaults_1(self):
        '''JS+

        function a(a, b, c=10) {
            return a + b + c;
        }

        print(a(1, 2) + a(2, 3, 4));

        %%
        22
        '''

    def test_utils_lang_jp_tr_func_defaults_2(self):
        '''JS+

        function a(a, b=a*a) {
            return a + b;
        }

        print(a(10) + a(2, 3));

        %%
        115
        '''

    def test_utils_lang_jp_tr_foreach_array(self):
        '''JS+

        Array.prototype.foo = '123';

        a = [1, 2, 3, 4];
        cnt = 0;

        for each (value in []) {
            cnt += 100000;
        }

        for each ([i] in a) {
            if (i == 3) {
                continue;
            }
            cnt += i;
        }

        print(cnt);

        %%
        7
        '''

    def test_utils_lang_jp_tr_foreach_obj(self):
        '''JS+

        Object.prototype.foo = '123';

        a = {'0': 1, '1': 2, '2': 3, '3': 4};
        cnt = 0;

        for each (value in {}) {
            cnt += 100000;
        }

        for each ([idx, value] in a) {
            cnt += parseInt(idx) * 100 + value * 1000;
        }

        for each (i in a) {
            if (i[1] == 3) {
                continue;
            }
            cnt += i[1];
        }

        for each (i in a) {
            if (i[1] == 3) {
                break;
            }
            cnt += i[1];
        }

        print(cnt);

        %%
        10610
        '''

    def test_utils_lang_jp_tr_foreach_str(self):
        '''JS+

        out = [];

        for each (ch in 'abc') {
            out.push(ch);
        }

        print(out.join('-'));

        %%
        a-b-c
        '''

    def test_utils_lang_jp_tr_for_in(self):
        '''JS+
        cnt = 0;

        a = {'10': 2, '20': 3}
        for (i in a) {
            if (i == '20') break;
            if (a.hasOwnProperty(i)) {
                cnt += parseInt(i);
            }
        }

        print(cnt);

        %%
        10
        '''

    def test_utils_lang_jp_tr_foreach_switch(self):
        '''JS+

        function a() {
            res = '';
            for each (v in [1]) {
                switch (42) {
                    case 42:
                        res += '-';
                    case 42:
                        res += '42';
                        break;
                }
                res += '-';
            }
            return res;
        }

        print(a());

        %%
        -42-
        '''

    def test_utils_lang_jp_tr_foreach_forin_cont(self):
        '''JS+

        function a() {
            res = '-';
            for each (v in [1]) {
                for (i in [2, 3]) {
                    if (i != '1') {
                        continue;
                    }
                    res += i;
                }
                res += '-';
            }
            return res;
        }

        print(a());

        %%
        -1-
        '''

    def test_utils_lang_jp_tr_foreach_while_cont(self):
        '''JS+

        function a() {
            res = '-';
            for each (v in [1]) {
                i = 0;
                while (i < 10) {
                    i ++;
                    if (i != 3) {
                        continue;
                    }
                    res += i;
                }
                res += '-';
            }
            return res;
        }

        print(a());

        %%
        -3-
        '''

    def test_utils_lang_jp_tr_foreach_dowhile_cont(self):
        '''JS+

        function a() {
            res = '-';
            for each (v in [1]) {
                i = 0;
                do {
                    i ++;
                    if (i != 3) {
                        continue;
                    }
                    res += i;
                } while (i < 10);
                res += '-';
            }
            return res;
        }

        print(a());

        %%
        -3-
        '''

    def test_utils_lang_jp_tr_foreach_for_cont(self):
        '''JS+

        function a() {
            res = '-';
            for each (v in [1]) {
                for (i = 0; i < 10; i++) {
                    if (i != 2) {
                        continue;
                    }
                    res += i;
                }
                res += '-';
            }
            return res;
        }

        print(a());

        %%
        -2-
        '''

    def test_utils_lang_jp_tr_for_plain(self):
        '''JS+
        cnt = 0;
        a = [10, 20, 30];
        for (i = 0, len = a.length, j=1000; i < len; i++, j+=1000) {
            if (j > 10e6) continue;
            cnt += i * j + a[i];
        }

        print(cnt);

        %%
        8060
        '''

    def test_utils_lang_jp_tr_try_1(self):
        '''JS+
        class E {}
        class E1(E) {}
        class E2(E) {}
        class E3(E) {}
        class EA(E2, E3) {}
        class E4() {}

        function t(n=0) {
            try {
                switch (n) {
                    case 0: throw E();
                    case 1: throw E1();
                    case 2: throw E2();
                    case 3: throw E3();
                    case 4: throw EA();
                    case 5: throw E4();
                }
            }
            except (E1 as ex) {
                e = '.' + ex.$cls.$name + '.';
            }
            except ([E2, E3] as ex) {
                e ='+' + ex.$cls.$name + '+';
            }
            except (E) {
                e = '-e-';
            }
            except {
                e = '=42=';
            }
            finally {
                if (e) {
                    e += '^';
                } else {
                    e = '^'
                }
            }

            return ' ' + e + ' ';
        }

        e = t() + t(100) + t(1) + t(2) + t(3) + t(4) + t(5);

        print(e);

        %%
        -e-^  ^  .E1.^  +E2+^  +E3+^  +EA+^  =42=^
        '''

    def test_utils_lang_jp_tr_try_2(self):
        '''JS+

        r = ''
        abc = null
        try {
            abc.foo
        }
        except {
            r += 'caught'
        }
        finally {
            r += '-and-fail'
        }

        print(r)

        %%
        caught-and-fail
        '''

    def test_utils_lang_jp_tr_try_3(self):
        '''JS+

        r = '';
        abc = null;

        try {
            try {
                abc.foo
            }
            finally {
                r += '-and-fail'
            }
        } except {}

        print(r)

        %%
        -and-fail
        '''

    def test_utils_lang_jp_tr_try_4(self):
        '''JS+

        r = '';
        abc = void(0);

        try {
            abc.foo
        } except {
            try {
                abc.foo
            }
            except {}
            finally {
                r += '-and-fail'
            }
        }

        print(r)

        %%
        -and-fail
        '''

    def test_utils_lang_jp_tr_try_5(self):
        '''JS+

        r = '';
        abc = null;

        try {
        }
        except {}
        else {
            try {
                abc.foo
            }
            except {}
            finally {
                r += '-and-fail'
            }
        }

        print(r)

        %%
        -and-fail
        '''

    def test_utils_lang_jp_tr_try_6(self):
        '''JS+

        r = '';
        abc = null;

        try {
        }
        except {}
        finally {
            try {
                abc.foo
            }
            except {}
            finally {
                r += '-and-fail'
            }
        }

        print(r)

        %%
        -and-fail
        '''

    def test_utils_lang_jp_tr_try_7(self):
        '''JS+

        r = '';

        class E {}

        try {
            throw '123';
        }
        except (BaseObject as e) {
            r += e;
        }
        finally {
            r += '-';
        }

        print(r)

        %%
        123-
        '''

    def test_utils_lang_jp_tr_try_8(self):
        '''JS+

        r = '';

        class E {}

        try {
            throw '123';
        }
        except (E) {
            r += 'E'
        }
        except (BaseObject) {
            r += 'smth'
        }
        finally {
            r += '-';
        }

        print(r)

        %%
        smth-
        '''

    def test_utils_lang_jp_tr_try_std_1(self):
        '''JS+

        r = '';

        try {
            throw '123';
        }
        catch (e) {
            r += '=' + e;
        }
        finally {
            r += '=';
        }

        try {
            throw '123';
        }
        catch (e) {
            r += '=' + e;
        }

        try {
            try {
                throw '123';
            }
            finally {
                r += 'finally'
            }
        }
        except {}

        print(r);

        %%
        =123==123finally
        '''

    def test_utils_lang_jp_tr_multiline_sq_string(self):
        r"""JS+
        a = '''''' + '''!''' + '''

        12

        '''

        print(a.replace(/\n/g, '~').replace(/\s/g, '.'))
        %%
        !~~........12~~........
        """

    def test_utils_lang_jp_tr_multiline_dq_string(self):
        r'''JS+
        a = """""" + """!""" + """

        12

        """

        print(a.replace(/\n/g, '~').replace(/\s/g, '.'))
        %%
        !~~........12~~........
        '''

    def test_utils_lang_jp_tr_with_1(self):
        '''JS+

        chk = '';

        class E {}

        class W1 {
            function enter() {
                nonlocal chk;
                chk += '-enter-';
                return {'a': 'b'};
            }

            function exit(exc) {
                nonlocal chk;
                chk += '-exit-';
                if (exc) {
                    chk += '(' + exc.$cls.$name + ')';
                } else {
                    chk += '()';
                }
                return true;
            }
        }

        with (W1() as w) {
            chk += w['a'];
        }

        chk += '|';

        with (W1() as w) {
            throw E();
        }

        print(chk)

        %%
        -enter-b-exit-()|-enter--exit-(E)
        '''

    def test_utils_lang_jp_tr_with_2(self):
        '''JS+

        chk = '';

        class W {
            function construct(name) {
                this.name = name;
                nonlocal chk;
                chk += 'create(' + name + ')-';
            }

            function enter() {
                nonlocal chk;
                chk += 'enter(' + this.name + ')-';
                return this;
            }

            function exit() {
                nonlocal chk;
                chk += 'exit(' + this.name + ')-';
            }
        }

        with (W('a0') as a0, W('a1'), W('a2')) {
            chk += '|' + a0.name + '|';
        }

        print(chk);

        %%

        create(a0)-enter(a0)-create(a1)-enter(a1)-create(a2)-enter(a2)-|a0|exit(a2)-exit(a1)-exit(a0)-
        '''

    def test_utils_lang_jp_tr_with_3(self):
        '''JS+
        try {
            with (1) {}
            print('fail');
        } catch (e) {
            e2 = e + '';
            if (e2.indexOf("context managers must") > 0) {
                print('ok');
            } else {
                throw e;
            }
        }

        %%
        ok
        '''

    def test_utils_lang_jp_tr_func_rest_1(self):
        '''JS+

        function test0(...a) {
            return a.join('+') + '~'
        }

        function test1(a, ...b) {
            return b.join('-') + '|';
        }

        function test2(a, b=10, ...c) {
            return '(' + b + ')' + c.join('*') + '$';
        }

        print(test0() + test0(1) + test0(1, 2) +
              test1(1) + test1(1, 2) + test1(1, 2, 3) +
              test2(1) + test2(1, 2) + test2(1, 2, 3) + test2(1, 2, 3, 4))

        %%
        ~1~1+2~|2|2-3|(10)$(2)$(2)3$(2)3*4$
        '''

    def test_utils_lang_jp_is_isnt(self):
        '''JS+

        print((1 is 1 isnt false is true) && (NaN is NaN));

        %%
        true
        '''

    def test_utils_lang_jp_is_instanceof(self):
        '''JS+

        class Foo {}
        class Bar(Foo) {}

        print((Bar() instanceof Foo) && ('bar' instanceof BaseObject)
              && ([] instanceof Array) && !([] instanceof String))

        %%
        true
        '''

    def test_utils_lang_jp_builtins_1(self):
        '''JS+

        print(isinstance(1, BaseObject) && 1 instanceof BaseObject);

        %%

        true
        '''

    def test_utils_lang_jp_builtins_2(self):
        '''JS+

        print(1 instanceof BaseObject);

        %%

        true
        '''

    def test_utils_lang_jp_builtins_3(self):
        '''JS+

        print(object.$name);

        %%
        object
        '''

    def test_utils_lang_jp_builtins_4(self):
        '''JS+

        print(object + type);

        %%
        <class object><class type>
        '''

    def test_utils_lang_jp_builtins_5(self):
        '''JS+

        object

        %%
        '''

    def test_utils_lang_jp_builtins_6(self):
        '''JS+

        print([1, object, type][0])

        %%
        1
        '''

    def test_utils_lang_jp_builtins_7(self):
        '''JS+

        print({'a': 'b', 'c': object}['a']);

        %%
        b
        '''

    def test_utils_lang_jp_builtins_8(self):
        '''JS+

        a = {'b' : {'c': function() { print('aaaa')}}};

        a.b.c();

        %%
        aaaa
        '''

    def test_utils_lang_jp_builtins_9(self):
        '''JS+

        new object()

        %%
        '''

    def test_utils_lang_jp_builtins_10(self):
        '''JS+

        print(typeof object)

        %%
        function
        '''

    def test_utils_lang_jp_builtins_11(self):
        '''JS+

        print(object['$name'])

        %%
        object
        '''

    def test_utils_lang_jp_builtins_12(self):
        '''JS+

        print(void object)

        %%
        undefined
        '''

    def test_utils_lang_jp_builtins_13(self):
        '''JS+

        print('abc' in object)

        %%
        false
        '''

    def test_utils_lang_jp_builtins_14(self):
        '''JS+

        print(object instanceof Object)

        %%
        false
        '''

    def test_utils_lang_jp_builtins_15(self):
        '''JS+

        print(isinstance((1, object), type))

        %%
        true
        '''

    def test_utils_lang_jp_builtins_16(self):
        '''JS+

        print((--object) + (type++))

        %%
        NaN
        '''

    def test_utils_lang_jp_builtins_17(self):
        '''JS+

        print((object ? '1' : '2') + (1 ? type : '3') + (0 ? 1 : BaseObject))

        %%
        1<class type><class BaseObject>
        '''

    def test_utils_lang_jp_builtins_18(self):
        '''JS+

        function a(a=object) {
            return a;
        }

        print(a()+'')

        %%
        <class object>
        '''
