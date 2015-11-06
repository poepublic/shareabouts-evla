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

@single-line: 3;
@single-halo: 5;
@shared-line: 2;
@shared-halo: 4;
@shared-offset: 1.5;
@combined-halo: 7;

/* ====================== */
/* Halos around the lines */
#blue-line,
#expo-line,
#gold-line,
#green-line,
#rp-lines {
  ::halo {
    line-width: @single-halo;
    line-color: @halo-color;
    line-join: round;
    line-cap: round;
  }
}

/* Special Cases:
 * - The blue-line and expo-line share track for portions,
 *   but they're in different layers.
 * - The red-line and purple-line are both in the rp layer.
 */
#blue-line::halo { line-offset: @shared-offset; }
#expo-line::halo { line-offset: -@shared-offset; }

#blue-line[shared=true],
#expo-line[shared=true] {
  ::halo {line-width: @shared-halo;}
}

#rp-lines[line="1"]::halo { line-offset: @shared-offset; }
#rp-lines[line="2"]::halo { line-offset: -@shared-offset; }
#rp-lines[line="3"]::halo { line-width: @combined-halo; }

/* ==================== */
/* The lines themselves */
#blue-line,
#expo-line,
#gold-line,
#green-line,
#rp-lines {
  ::track {
    line-width: @single-line;
    line-join: round;
    line-cap: round;
  }
}

#blue-line::track { line-color: @blue; }
#expo-line::track { line-color: @expo; }
#gold-line::track { line-color: @gold; }
#green-line::track { line-color: @green; }
#rp-lines[line="1"]::track { line-color: @red; }
#rp-lines[line="2"]::track { line-color: @purple; }

/* Special Cases */
#blue-line::track { line-offset: @shared-offset; }
#expo-line::track { line-offset: -@shared-offset; }

#blue-line[shared=true],
#expo-line[shared=true] {
  ::track {line-width: @shared-line;}
}

#rp-lines[line="1"]::track { line-offset: @shared-offset; }
#rp-lines[line="2"]::track { line-offset: -@shared-offset; }
#rp-lines[line="3"]::track { line-width: 0; }

#rp-lines[line="3"] {
  ::red-track {
    line-width: @shared-line;
    line-color: @red;
    line-offset: @shared-offset;
  }
  ::purple-track {
    line-width: @shared-line;
    line-color: @purple;
    line-offset: -@shared-offset;
  }
}
/*
#rail-stations {
  line-width: 1;
  line-color: rgba(68,255,170,0.5);
}
*/
