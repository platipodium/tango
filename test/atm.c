
#include <stdlib.h>
#include <mpi.h>

#define NUM_TIMESTEP 100
#define SECS_PER_TIMESTEP 1

int main(int argc, char* argv[])
{
    double *air_temp;
    double *shortwave_flux;
    int i, time;
    
    air_temp = (double*)malloc(10 * sizeof(double));
    shortwave_flux = (double*)malloc(10 * sizeof(double));

    MPI_Init(&argc, &argv);

    time = 0;
    for (i = 0; i < NUM_TIMESTEPS; i++) {
        tango_begin_comm(time);
        tango_send(air_temp);
        tango_send(shortwave_flux);
        tango_end_comm();

        time += SECS_PER_TIMESTEP;
    }

    MPI_Finalize();

    free(air_temp);
    free(shortwave_flux);
}
