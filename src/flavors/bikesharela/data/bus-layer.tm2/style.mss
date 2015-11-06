Map {
  background-color: rgba(255,255,255,0);
}

#bus-lines {
  ::buffer {
    line-width: 3;
    line-color: white;
    
    [zoom>17] {
      line-width: 5;
    }
  }
  
  line-width: 1;
  line-color: #666;

  [zoom>17] {
    line-width: 3;
  }
}
