# -*- coding: utf-8 -*-
import pytest

from sensirion_driver_support_types.mixin_access import MixinAccess


class Abase:

    def __init__(self, name):
        self._name_a = name

    def get_name(self):
        return self._name_a

    def my_private_name(self):
        return 'private_name:' + self._name_a

    @staticmethod
    def static_fun():
        return 'a_static_fun'


class Bbase:

    def __init__(self, name):
        self._name_b = name

    @property
    def name(self):
        return self._name_b

    @name.setter
    def name(self, value):
        self._name_b = value

    def get_name(self):
        return self._name_b

    @classmethod
    def class_fun(cls):
        return 'b_class_fun'

    @staticmethod
    def static_fun():
        return 'b_static_fun'

    @staticmethod
    def my_static_fun():
        return 'b_my_static_fun'


class SimpleSingle(Abase):
    """This is the way the current drivers are generated"""
    base = MixinAccess()

    def __init__(self):
        self.base.__init__('a_base')


class Single(Abase):
    """This is the way how drivers have to be generated such that thy can be used as base class"""
    base = MixinAccess(Abase)

    def __init__(self):
        self.base.__init__('a_base')


class Multiple(Abase, Bbase):
    a_base = MixinAccess(Abase)
    b_base = MixinAccess(Bbase)

    def __init__(self):
        super().__init__('a_base')
        super(Abase, self).__init__('b_base')
        print(self.__class__.__bases__)

    def get_all_names(self):
        return f'{self.a_base.get_name()}\n{self.b_base.get_name()}'


class DeriveSingle(Single):
    ...


class DeriveMultiple(Multiple):
    ...


@pytest.mark.parametrize("cls", [SimpleSingle(), Single(), DeriveSingle()])
def test_single_base_access(cls):
    assert cls.base.get_name() == 'a_base', "error calling member function with only one base class"


@pytest.mark.parametrize("cls", [SimpleSingle(), Single(), DeriveSingle()])
def test_single_static_base_access(cls):
    assert cls.base.static_fun() == 'a_static_fun', "error calling static function with only one base class"


@pytest.mark.parametrize("cls", [Multiple(), DeriveMultiple()])
def test_multiple_base_access(cls):
    assert cls.a_base.get_name() == 'a_base', "error calling member function in base class 0"
    assert cls.b_base.get_name() == 'b_base', "error calling member function in base class 1"


@pytest.mark.parametrize("cls", [Multiple(), DeriveMultiple()])
def test_multiple_class_base_access(cls):
    # cls = Multiple()
    assert cls.a_base.static_fun() == 'a_static_fun', "error calling static function on superclass 0"
    assert cls.b_base.class_fun() == 'b_class_fun', "error calling static function on superclass 1"
    assert cls.get_all_names() == 'a_base\nb_base', "error using selector within member function of derived class"

    assert cls.b_base.my_static_fun() == 'b_my_static_fun', 'error calling static function without duplicate'
    assert cls.a_base.my_private_name() == 'private_name:a_base', 'error calling member function without duplicate'
