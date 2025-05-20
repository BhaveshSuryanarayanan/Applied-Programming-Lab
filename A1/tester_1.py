import unittest
import time
import matmul as ml
import stressen_matmul as sml
import numpy as np

def normal(A,B):
    return ml.matrix_multiplication(A,B)

def strassen(A,B):
    return sml.matrix_multiply(A,B)

class TestProgram(unittest.TestCase):
    def test_output(self):
        m,n,k = 100,100,100
        a = np.random.randint(0, 101, size=(m, n))
        b = np.random.randint(0, 101, size=(n, k))
        self.assertTrue(np.array_equal(normal(a,b),strassen(a,b)),'outputs donot match')
         
    def test_execution_time(self):
        m, n, k = 128, 128, 128
        a = np.random.randint(0, 101, size=(m, n))
        b = np.random.randint(0, 101, size=(n, k))
        
        # Measure execution time of normal multiplication
        start_time = time.time()
        normal(a, b)
        normal_duration = time.time() - start_time
        
        # Measure execution time of Strassen multiplication
        start_time = time.time()
        strassen(a, b)
        strassen_duration = time.time() - start_time
        
        # Print execution times
        print(f"Normal multiplication duration: {normal_duration} seconds")
        print(f"Strassen multiplication duration: {strassen_duration} seconds")
        
        # Assert that normal multiplication is not significantly slower than Strassen
        self.assertLessEqual(normal_duration, strassen_duration * 10, "Normal multiplication is more than 10 times slower than Strassen")

if __name__ == '__main__':
    unittest.main()
    