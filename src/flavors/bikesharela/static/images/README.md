Each of the sites to survey can have a set of thumbnail images attached to it. These will appear gallery-style in the site detail.

To add images to a site, first give that site a `Site_ID` attribute. Then, in the *static/images/metadata/* folder in the flavor, create a file called *<Site_ID>_images.json*. For example, if a site has an id of `"0001_001"`, then you should create a JSON file named *0001_001_images.json*.

Inside of this JSON file should be a list of image file names. For example, in your *0001_001_images.json* file you may have:

```json
{"images": ["0001_001_1.JPG", "0001_001_2.JPG", "0001_001_3.JPG"]}
```

Each of these image file names should correspond to an image in *static/images/scaled/* in your flavor folder.
