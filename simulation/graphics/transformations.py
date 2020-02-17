import pygame
import numpy as np

def vector_to_array(vector: pygame.Vector3):
    return np.array([[vector.x], [vector.y], [vector.z]])

def array_to_vector(array: np.ndarray):
    return pygame.Vector3(array[0], array[1], array[2])

def rotationMatrix(axis: pygame.Vector3, angle: float):
    length = np.sqrt(axis.x**2 + axis.y**2 + axis.z**2)
    axis.x /= length
    axis.y /= length
    axis.z /= length
    
    mat = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    mat[0, 0] = axis.x**2 * (1 - np.cos(angle)) + np.cos(angle)
    mat[0, 1] = axis.y * axis.x * (1 - np.cos(angle)) - axis.z * np.sin(angle)
    mat[0, 2] = axis.z * axis.x * (1 - np.cos(angle)) + axis.y * np.sin(angle)

    mat[1, 0] = axis.x * axis.y * (1 - np.cos(angle)) + axis.z * np.sin(angle)
    mat[1, 1] = axis.y**2 * (1 - np.cos(angle)) + np.cos(angle)
    mat[1, 2] = axis.z * axis.y * (1 - np.cos(angle)) - axis.x * np.sin(angle)

    mat[2, 0] = axis.x * axis.z * (1 - np.cos(angle)) - axis.y * np.sin(angle)
    mat[2, 1] = axis.y * axis.z * (1 - np.cos(angle)) + axis.x * np.sin(angle)
    mat[2, 2] = axis.z**2 * (1 - np.cos(angle)) + np.cos(angle)

    return mat

def applyTransformation(transformation_matrix: np.ndarray, vector: pygame.Vector3):
    return array_to_vector(transformation_matrix.dot(vector_to_array(vector)))