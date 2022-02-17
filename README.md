# Choose visually distinct N-sized colour palettes from a list of colours
In our product, we display driving route lines on a map.
Customers usually have between 5 and 30 routes, and by default
our product automatically chooses the colours for them.


## Colour Palette Criteria
Colours in a palette must be:
- Visually distinct from each other
- Visually distinct from colours on the map
- Reasonably visible (not too light or dark)
- Aesthetically pleasing

## Approach

1. Create a shortlist of colours which are all aesthetically pleasing, and meet our criteria
2. Split these colours into N groups which are as visually distinct as possible
3. Choose a colour from (or generate a colour based on) each group to create our palette


## The Shortlist
The aim of making a shortlist is to ensure that all colours are "visually pleasing".  
Of course, this is subjective, but I can at least remove jarring colours (like #FF0000 , #00FF00 and #0000FF for example).

I hand picked colours from a [Canva article with 100 colour palettes](https://www.canva.com/learn/100-color-combinations/)
and put them in [colours.py](colours.py)


I mostly accepted all the colours, except:
- Whites, greys and blacks, since they're boring
- Colours which are too light to use as a background with white text

There are ~230 colours in the shortlist.  
You can see them in [all_colours.html](https://htmlpreview.github.io/?https://github.com/treharne/colours/blob/main/all_colours.html)

It's worth noting that many are quite similar!


## Group the colours
We need an algorithm which can:
- Group the colours into a [predetermined number of groups](https://en.wikipedia.org/wiki/Cluster_analysis#Centroid-based_clustering)
- Do this based on some kind of distance metric: Colours in the same group should be the most similar

[K-means](https://en.wikipedia.org/wiki/K-means_clustering) seems like a good choice!  
I'll use [Scikit-learn K-means](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) for this project.

### Problem: Bad Clusters
The first time I ran the algorithm using RGB values for each colour, there were some pretty good clusters:

![Good red cluster using RGB](media/rgb_good_cluster_red.png)
![Good green cluster using RGB](media/rgb_good_cluster_green.png)

but also some clusters which seemed "bad" in my opinion: 

![Bad dark cluster using RGB](media/rgb_bad_cluster_dark.png)
![Bad light cluster using RGB](media/rgb_bad_cluster_light.png)

The goal of this project is to get colours that are visually distinct into different clusters. But many colours in this cluster are quite visually distinct.... so shouldn't they be in different clusters?

I can understand why the algorithm did it like this - it seems like they're all fairly dark colours on the left, or fairly light colours on the right.

But I want to do better.

(if you're curious, you can see the results with N=15 using RGB in [clustered_colours_rgb.html](https://htmlpreview.github.io/?https://github.com/treharne/colours/blob/main/clustered_colours_rgb.html))

### Solution: Better Colour Representation
Wow... colour theory is a rabbit hole.

TLDR:
- The (euclidean) distance between two RGB colours doesn't represent very well how differently we perceive them
- There's an alternative notation for colours called `L*a*b`, which is [designed to better represent human colour perception](https://en.wikipedia.org/wiki/CIELAB_color_space#Advantages).


So I converted all my colours from RGB into `L*a*b` before clustering them.

This *substantially* improved the groupings:

![Good yellow cluster using LAB](media/lab_good_cluster_yellow.png)
![Good pink cluster using LAB](media/lab_good_cluster_pink.png)

![Good blue cluster using LAB](media/lab_good_cluster_blue.png)
![Good orange cluster using LAB](media/lab_good_cluster_orange.png)

## Choose a colour from each Palette
There are a few obvious approaches here:
- Randomly choose a colour from each group
- Take the mean of each group
- Take the median of each group (what does this mean?)

Since I was using K-means, the simplest was to take the mean.



# Results


## Random vs RGB vs `L*a*b`
**Random colours from Shortlist**  

![Random Palette](media/random_centres.png)

Quite a few colours have very close pairs.

**RGB + K-means**  

![RGB Palette](media/rgb_centres.png)

Some close pairs

**`L*a*b` + K-means**  

![LAB Palette](media/lab_centres.png)


Fewer close pairs. Pinks and browns are arguably worse than RGB. Greens, blues, yellows definitely better than RGB.

Of course, as always, this is subjective.


## Colour Palettes of for N <= 40
[colour_palettes.html](https://htmlpreview.github.io/?https://github.com/treharne/colours/blob/main/colour_palettes.html) has the colour palettes generated using this methodology (K-means on `L*a*b`) for each palette size from 1 to 40.

[colour_palettes.json](colour_palettes.json) has the same colours, but as json.  
You can get each palette from this file using
```python
# n is the number of colours you need in your palette
colour["palettes"][n]
```
