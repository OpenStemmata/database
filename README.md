# Open Stemmata Database

This repository contains an open source collection of historical text genealogies, in forms of tree-like graphs (stemma) for a variety of languages.

## Contributing

Find more information on the [**project website**](https://openstemmata.github.io/).

### Sending your contribution

You can contribute by sending us images and/or metadata and DOT files,

- by making a **pull request** on the main branch (preferred);
- by opening [**an issue**](https://github.com/OpenStemmata/database/issues/13);
- by sending it to us via email, to OpenStemmata \[at\] protonmail.com.

If you wish to contribute, have a look at the [examples](https://github.com/OpenStemmata/database/tree/main/examples) folder:

It contains several cases:

- a simple case, but with very complete metadata: [Segre_1971_Roland](https://github.com/OpenStemmata/database/tree/main/examples/Segre_1971_Roland)
- a slightly more complex case: [Paris_1872_Alexis](https://github.com/OpenStemmata/database/tree/main/examples/Paris_1872_Alexis)

You can also read our more detailed [Guidelines](https://openstemmata.github.io/guidelines.html) !

### Organisation of a record

Actual data is stored in the [data](https://github.com/OpenStemmata/database/tree/main/data) folder, and are sorted by linguistic code (e.g., `fro` for Old French traditions; `gmh` for Middle High German).

Each record is contained in a dedicated folder, and can contain up to three elements:

- `stemma.png`: scan from the source edition;
- `metadata.txt`: metadata file about the stemma
- `stemma.gv`: GraphViz DOT format file for the stemma.

### Generating metadata and DOT files

The following resources can help you create the necessary files:

- [Our form metadata creator](https://openstemmata.github.io/document-your-stemma.html): just fill up the form and get the txt content. 
- [**Edotor**](https://edotor.net/?engine=dot?engine=dot#%23%20Place%20the%20cursor%20inside%20%22graph%22%20to%20get%20some%20refactoring%20options%0A%0Adigraph%20%7B%0A%0A%20%20%20%20%23%20To%20refactor%20nodes%2C%20place%20the%20cursor%20left%20to%20a%20node%20name%0A%20%20%20%20omega%20-%3E%20b%3B%0A%20%20%20%20omega%20-%3E%20c%3B%0A%20%20%20%20c%20-%3E%20d%3B%0A%20%20%20%20c%20-%3E%20e%3B%0A%20%20%20%20omega%20-%3E%201%3B%20%0A%20%20%20%201%20-%3E%20a%20%23%20use%20numbers%20for%20unlabelled%20nodes%20in%20the%20source%20stemma%0A%20%20%20%201%20-%3E%20aprime%0A%0A%20%20%20%20%23%20Hover%20over%20color%20names%20to%20get%20a%20color%20picker%0A%20%20%20%20b%20-%3E%20e%20%5Bstyle%3D%22dashed%22%5D%0A%20%20%20%20b%20-%3E%20c%20%5Bdir%3Dnone%2C%20style%3D%22dashed%22%5D%3B%20%23%20for%20the%20exception%20where%20an%20undirected%20link%20is%20existant.%0A%0A%20%20%20%20%23%20Grey%20color%20is%20used%20for%20hypothetical%20nodes%3B%20labels%20can%20be%20redefined%20if%20needed%0A%20%20%20%20omega%20%5Bcolor%3D%22grey%22%5D%3B%0A%20%20%20%201%20%5Bcolor%3D%22grey%22%2C%20label%3D%22%22%5D%3B%20%0A%20%20%20%20aprime%5Blabel%3D%22a'%22%5D%0A%0A%7D%0A): a free online DOT editor with graphical view.

DOT format is quite easy to master, and uses the following patterns:

- `a -> b` link from a to b
- `a -> b [style="dashed"]` dashed link from a to b (contamination)
- `a -> b [style="dashed"]` grey link from a to b (uncertainty)
- `alpha[color="grey", label="α"]` color alpha in grey (for hypothetical nodes, i.e., not extant manuscripts) and label it properly.

**<span style="color:red">If you're hesitant, head over to the online [*editor*](https://edotor.net/?engine=dot?engine=dot#%23%20Place%20the%20cursor%20inside%20%22graph%22%20to%20get%20some%20refactoring%20options%0A%0Adigraph%20%7B%0A%0A%20%20%20%20%23%20To%20refactor%20nodes%2C%20place%20the%20cursor%20left%20to%20a%20node%20name%0A%20%20%20%20omega%20-%3E%20b%3B%0A%20%20%20%20omega%20-%3E%20c%3B%0A%20%20%20%20c%20-%3E%20d%3B%0A%20%20%20%20c%20-%3E%20e%3B%0A%20%20%20%20omega%20-%3E%201%3B%20%0A%20%20%20%201%20-%3E%20a%20%23%20use%20numbers%20for%20unlabelled%20nodes%20in%20the%20source%20stemma%0A%20%20%20%201%20-%3E%20aprime%0A%0A%20%20%20%20%23%20Hover%20over%20color%20names%20to%20get%20a%20color%20picker%0A%20%20%20%20b%20-%3E%20e%20%5Bstyle%3D%22dashed%22%5D%0A%20%20%20%20b%20-%3E%20c%20%5Bdir%3Dnone%2C%20style%3D%22dashed%22%5D%3B%20%23%20for%20the%20exception%20where%20an%20undirected%20link%20is%20existant.%0A%0A%20%20%20%20%23%20Grey%20color%20is%20used%20for%20hypothetical%20nodes%3B%20labels%20can%20be%20redefined%20if%20needed%0A%20%20%20%20omega%20%5Bcolor%3D%22grey%22%5D%3B%0A%20%20%20%201%20%5Bcolor%3D%22grey%22%2C%20label%3D%22%22%5D%3B%20%0A%20%20%20%20aprime%5Blabel%3D%22a'%22%5D%0A%0A%7D%0A) for creating the file !</span>**

## License

Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
