Map {
  background-color: rgba(0,0,0,0);
}

@blue: #0171BB;
@green: #6EBE69;
@gold: #FFB613;
@purple: #A55DA9;
@red: #E22A32;
@expo: #01A4E5;
@halo-color: rgba(255,255,255,1);

#bikeways {
  ::halo {
    line-width: 2;
    line-color: @halo-color;
    line-join: round;
    line-cap: round;
    
    [zoom>=12] {
      line-width: 3;
      line-color: rgba(255,255,255,0.9)
    }
    [zoom>=14] {
      line-width: 4;
      line-color: rgba(255,255,255,0.7)
    }
  }

  [zoom<12] {
    line-width: 1;
  }
  [zoom>=12] {
    line-width: 2;
    line-dasharray: 2,2;
  }
  [zoom>=14] {
    line-width: 3;
    line-dasharray: 3,3;
  }
  line-color: rgba(17, 133, 55, 0.87);
}

