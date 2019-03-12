# cas-assignment #
Assignment for the Computer Assisted Surgery course @ University of Bern

## Installation ##

* Install Conda and VSCode
* `conda env create --file environment.yml` use the Conda terminal!
* `activate cas` use the Conda terminal!

## Run a File ##

Using `python cas\test_installation.py`

# Assignments #

## Assignment 1 - Planning ##

![result assignment planning](assignments/planning/result.png)
> Result of the planning assigment

There are many ways of implementing region growing algorithms for image segmentation. The two most famous algorithms are Flood fill and the Watershed algorithm. Both have its pros and cons. As Flood fill is fast but less smooth, Watershed points with smooth but slower processing. The current implementation in this assignment is based on the Flood fill algorithm. It was much easier to implement and it is also fast. Additionally, the algorithm would provide a radius parameter. In our case, this leads to much worse results as the resolution of the data is very narrow.
So the main point in our algorithm is to choose a neighbor with a radius of one and compare it with the seed point. The sensitivity parameter in the algorithm defines how much the intensity value of the voxel can differ from this seed point. If it's in the range it becomes a candidate for further explorations of additional neighbors. So in our algorithm, every voxel in the very neighborhood can only differ with an absolute value of 40.
On your segmentation mask, two vertebrae are connected by 1 voxel. 

### Which morphological operator could you use to separate these two regions? ###
The most basic morphological operations are dilation and erosion. In this case, an erosion-based algorithm would be the most suitable, as it groups voxels with similar values. The structure, for example, the disks in the spinal cord have small spaces in between them. That is enough for the algorithm to group them.

### Your CT image has salt & pepper noise. How would you preprocess the image to improve your segmentation? ###
A median filter our a Gauss filter would come handy in this situation. The Gausfillter would make the noise and the whole image blurry. The median filter can handle the noise much better and in the end, the noise is almost not visible any more.

### You want to plan a trajectory for a pedicle screw placement on your 3D model. What information do you need to define this trajectory? ###

From an image perspective, structures with high intensity are interesting for the planning as it could indicate veins, nerves or bones. So good segmentation is mandatory to find a clear path to the goal.

### Which algorithm can you use to get a surface model from your segmentation? ###
The keyword is edge detection. The surface of an object separates two intensity region in the body. An example would be bone and muscle. Many algorithms, such as morphological or gradient based can be used.


### If you downsample your 3D CT image by a factor of 2 in all dimensions, how much faster or slower will your algorithm get? ###
Let's imagine a cube with the edge of 100 by 100 by 100. The cube would have a volume of 100 to the third power. This equals to 100000. So by shorting all edges by half, wight would equal to a cube of 50 by 50 by 50 with a volume of 125000. The volume correspondents to our voxels in our image. Cutting the edge by half gives us 8 times fewer voxels. So an algorithm would be 8 times faster, as it just has to process an 8th.
