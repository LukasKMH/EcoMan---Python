import unittest
from scripts.vetor import Vector2  # Assumindo que a classe Vector2 está no arquivo vector2.py
import math

class TestVector2(unittest.TestCase):

    def test_initialization(self):
        """
        Testa se a inicialização do vetor está correta.
        """
        v = Vector2(3, 4)
        self.assertEqual(v.x, 3)
        self.assertEqual(v.y, 4)

    def test_addition(self):
        """
        Testa a adição de dois vetores.
        """
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        v3 = v1 + v2
        self.assertEqual(v3, Vector2(4, 6))


    def test_negation(self):
        """
        Testa a negação de um vetor.
        """
        v = Vector2(2, -3)
        neg_v = -v
        self.assertEqual(neg_v, Vector2(-2, 3))

    def test_multiplication(self):
        """
        Testa a multiplicação de um vetor por um escalar.
        """
        v = Vector2(2, 3)
        v_mult = v * 3
        self.assertEqual(v_mult, Vector2(6, 9))


    def test_equality(self):
        """
        Testa a igualdade de dois vetores considerando o limite de precisão.
        """
        v1 = Vector2(1.0000001, 1.0000001)
        v2 = Vector2(1.0000002, 1.0000002)
        self.assertTrue(v1 == v2)


    def test_as_tuple(self):
        """
        Testa a conversão do vetor para uma tupla.
        """
        v = Vector2(7, 8)
        self.assertEqual(v.asTuple(), (7, 8))

    def test_as_int(self):
        """
        Testa a conversão dos componentes do vetor para inteiros.
        """
        v = Vector2(7.9, 8.1)
        self.assertEqual(v.asInt(), (7, 8))

    def test_str(self):
        """
        Testa a representação em string do vetor.
        """
        v = Vector2(9, 10)
        self.assertEqual(str(v), "<9, 10>")

if __name__ == '__main__':
    unittest.main()
