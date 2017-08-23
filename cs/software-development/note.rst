- workflow

  A commit to your source revision control system would trigger a build on your CI
  system, which would then push a new image to your Docker Registry if the build is
  successful. A notification from the Registry would then trigger a deployment on a
  staging environment, or notify other systems that a new image is available.
