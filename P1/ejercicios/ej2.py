"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 0

	Ejercicio 2
	Programe un par de funciones de ordenación de matrices (UNIDIMENSIONALES)
	de números distintas (burbuja, selección, inserción, mezcla, montículos...).
	Realice un programa que genere aleatoriamente matrices de números aleatorios
	y use dicho métodos para comparar el tiempo que tardan en ejecutarse.
"""
import random
import time

# O(n²)
def bubblesort(array):
	n = len(array)
	# Límite
	for i in range(1,n):
		# Subir la burbuja
		for j in range(0, n-i):
			if array[j] > array[j+1]:
				array[j], array[j+1] = array[j+1], array[j]

# O(n log(n))
def quicksort(array, threshold=3):
	n = len(array)
	# Si el array no lleva al tamaño mínimo, se ordena
	# con uno de los métodos clásicos
	if(n <= threshold):
		sorted_arr = array.copy()
		#print("Antes de bubble: ",sorted_arr)
		bubblesort(sorted_arr)
		#print("Después de bubble: ",sorted_arr)
		return sorted_arr
	else:
		# Seleccionamos un elemento pivote y particionamos el array para que
		# todos los elementos a la izquierda del pivote sean menores que él,
		# y que todos los que estén a la sean
		"""
		print("Antes de particionar:")
		print(array)
		print('Intermedio ',array[n//2])
		"""
		p, part_array = partition(array)
		"""
		print("Después de particionar:")
		print(part_array)
		print('Pivote ',part_array[p])
		print("----------------------------------------")
		"""

		# Ordenamos por separado las partes del vector
		first_part = quicksort(part_array[0:p])
		second_part = quicksort(part_array[p:n])

		# Recomponemos el vector
		return (first_part + second_part)


# Particionar el array
# Devuelve la posición del elemento pivote y el array particionado
def partition(array):
	arr = array.copy()
	n = len(arr)
	pivot = arr[n-1]
	i = 0
	for j in range(n):
		if arr[j] < pivot:
			arr[i],arr[j] = arr[j],arr[i]
			i += 1
	arr[i],arr[n-1] = arr[n-1],arr[i]
	return i, arr

def generate_random_array(max_length=50):
	length = random.randint(2,max_length)
	array = []
	for i in range(length):
		array.append(random.randint(0, length*length))
	return array


if __name__ == '__main__':
	rand_arr = generate_random_array()

	# Ejecutar y medir tiempo del bubblesort
	bubble_start = time.time()
	arr_bubble = rand_arr.copy()
	bubblesort(arr_bubble)
	bubble_end = time.time()
	bubble_time = bubble_end - bubble_start


	# Ejecutar y medir tiempo del quicksort
	quick_start = time.time()
	arr_quick = quicksort(rand_arr)
	quick_end = time.time()
	quick_time = quick_end - quick_start

	print('Array a ordenar:')
	print(rand_arr)
	print()
	print('Array ordenado por bubblesort:')
	print(arr_bubble)
	print()
	print('Tiempo ejecución bubblesort: {:.10f}'.format(bubble_time))
	print('Array ordenado por quicksort:')
	print(arr_quick)
	print()
	print('Tiempo ejecución quicksort: {:.10f}'.format(quick_time))


	"""
	test_arr = [9,3,6,1,2,8,15,22,7,89,4]


	arr_bubble = test_arr.copy()
	bubblesort(arr_bubble)



	arr_quick = quicksort(test_arr)




	rand_arr = generate_random_array()
	print(test_arr)
	print(arr_bubble)
	print(arr_quick)
	"""
