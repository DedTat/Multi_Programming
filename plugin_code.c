#include "math.h"
#include <stdio.h>
#include <stdlib.h>

void GenerateMatrix(float* A, float* B, float* C, int nDim)
{
	for (int i  = 0; i < nDim; i++)
    	for (int j = 0; j < nDim; j++)
    		A[i*nDim +j] = B[i*nDim +j] + C[i*nDim +j];
}

void PrepareMatrix(float* L, float* U, float* A, int nDim)
{
	for (int i  = 0; i < nDim; i++)
    	for (int j = 0; j < nDim; j++)
    		A[i*nDim +j] = A[i*nDim +j] + A[i*nDim +j];

	for (int i  = 0; i < nDim; i++)
  	{
    	for (int j = 0; j < nDim; j++)
    	{
      		L [i*nDim + j] = 0;
      		U [i*nDim + j] = 0;

      		if (i == j)
        		U[i*nDim + j] = 1;
    	}
  	}
}

void PrintMatrix(float* arr, int nDim)
{
	printf("%d elements\n", nDim);

	for (int i = 0; i < nDim; i++)
	{
		for (int j = 0; j < nDim; j++)
		{
			printf("%.2f ", arr[j + nDim*i]);
		}
		printf("\n");
	}
}

void FirstColRow(float* L, float* U, float* A, int nDim)
{
	for (int i = 0; i < nDim; i++)
  	{
    	L [i*nDim] = A [i*nDim];
    	U [i] = A [i] / L [0];
  	}
}

float SumForL(float* L, float* U, int nDim, int i, int j)
{
	float sum = 0;

	for (int k = 0; k < j; k++)
    	sum += L [i*nDim + k] * U [k*nDim + j];

	return sum;
}

float SumForU(float* L, float* U, int nDim, int i, int j)
{
	float sum = 0;

	for (int k = 0; k < i; k++)
    	sum += L [i*nDim + k] * U [k*nDim + j];

	return sum;
}

void Solve(float* L, float* U, float* A, int nDim)
{
	float sum = 0;

	for (int i = 1; i < nDim; i++)
  	{
    	for (int j = 1; j < nDim; j++)
      	{
        	if (i >= j)
          	{
          		sum = 0;
              	sum = SumForL(L, U, nDim, i, j);
              	L[i*nDim + j] = A [i*nDim + j] - sum;
          	}
          	else
          	{
          		sum = 0;
          		sum = SumForU(L, U, nDim, i, j);
              	U[i*nDim + j] = (A [i*nDim + j] - sum) / L [i+i*nDim];
          	}
      	}
  	}
}

void LU(float* L, float* U, float* R, int nDim)
{
	for (int i = 0; i < nDim; i++)
	{
		for(int j = 0; j < nDim; j++)
		{
			R[i*nDim + j] = 0;

			for (int k = 0; k < nDim; k++)
				R[i*nDim +j] += L [i*nDim + k] * U [k*nDim + j];
		}
	}
}

void Discrepancy(float* A, float* R, float* Check, int nDim)
{
	for (int i  = 0; i < nDim; i++)
    	for (int j = 0; j < nDim; j++)
    		Check[i*nDim +j] = A[i*nDim +j] - R[i*nDim +j];
}


void TotalDisrep(float* Check, float* total, int nDim)
{
	for (int i  = 0; i < nDim; i++)
    	for (int j = 0; j < nDim; j++)
    		total[0] += Check[i*nDim +j];
}

void cFunc(float* A, float* B, float* C, float* L, float* U,
		   float* R, float* Check, float* total, int nDim)
{
	GenerateMatrix(A, B, C, nDim);
	PrepareMatrix(L, U, A, nDim);
	FirstColRow(L, U, A, nDim);
	Solve(L, U, A, nDim);
	LU(L, U, R, nDim);
	Discrepancy(A, R, Check, nDim);
	TotalDisrep(Check, total, nDim);
}
