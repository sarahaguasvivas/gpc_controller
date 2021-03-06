#ifndef __MATRIX_H__
#define __MATRIX_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <math.h>
#include <stdlib.h>

struct Matrix2{
    int rows;
    int cols;
    float *data = NULL;
    float *original_data_pointer = NULL;
    float tiny = 1e-20; // very small number
};

void set(struct Matrix2 & a, int rows, int cols);
void set_to_zero(struct Matrix2 &);
void set_to_ones(struct Matrix2 &); 
struct Matrix2 transpose(struct Matrix2);
struct Matrix2 add (struct Matrix2, struct Matrix2);
struct Matrix2 subtract (struct Matrix2, struct Matrix2);
struct Matrix2 scale(float, struct Matrix2);
struct Matrix2 multiply(struct Matrix2, struct Matrix2);
struct Matrix2 hadamard(struct Matrix2, struct Matrix2);
struct Matrix2 inverse (struct Matrix2);
void release(Matrix2 a);
void lubksb(struct Matrix2, int *, float *);
void ludcmp(struct Matrix2, int *, float *);
void equal(struct Matrix2 &, struct Matrix2);
struct Matrix2 nr_optimizer(struct Matrix2, struct Matrix2, struct Matrix2);
struct Matrix2 solve_matrix_eqn(struct Matrix2, struct Matrix2);

#ifdef __cplusplus
}
#endif
#endif