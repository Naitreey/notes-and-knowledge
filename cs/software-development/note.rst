time estimation
===============

continuous integration
======================

- workflow

  A commit to your source revision control system would trigger a build on your CI
  system, which would then push a new image to your Docker Registry if the build is
  successful. A notification from the Registry would then trigger a deployment on a
  staging environment, or notify other systems that a new image is available.

service-oriented architecture
=============================

microservices
-------------
- The philosophy of the microservices architecture essentially equals to the Unix
  philosophy of "Do one thing and do it well".

- The services are small - fine-grained to perform a single function.

- The organization culture should embrace automation of testing and deployment.

- Each service is elastic, resilient, composable, minimal, and complete.
