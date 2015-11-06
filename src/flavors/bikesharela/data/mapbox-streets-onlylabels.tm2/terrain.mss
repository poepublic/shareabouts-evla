#contour.label::label[index>=5] {
  text-name: "[ele]+' m'";
  text-face-name: 'Open Sans Regular';
  text-placement: line;
  text-size: 8;
  text-fill: #666;
  text-avoid-edges: true;
  text-halo-fill: fadeout(@crop,80%);
  text-halo-radius: 2;
  text-halo-rasterizer: fast;
  text-min-distance: 50;
}