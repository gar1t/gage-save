# Run lifecycle

A Gage run can have the following states:

- Not existing
- Pending - Gage is creating the run but it's otherwise undefined
  - Inferred by existence of meta dir containing PENDING marker
  - Meta dir under way, exists with PENDING marker
  - Run dir under way, may or may not exist


A Gage run is made up of a number of parts:

- A `.meta` directory, which is represented by `.meta.zip` after the run
  is finalized
- A `.run` directory
