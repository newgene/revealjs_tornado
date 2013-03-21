My browser-based slides using [reveal.js](https://github.com/hakimel/reveal.js) and [tornado](http://www.tornadoweb.org/). Markdown rendering is done by [Python-Markdown](https://pypi.python.org/pypi/Markdown). Reveal.js has a feature to [include markdown directly in the HTML template](https://github.com/hakimel/reveal.js#markdown), but markdown rendering is somewhat limited.

Install tornado, Markdown using

   
    pip install tornado Markdown


To view slides, run

   
    python view_slides.py [--debug]


, and then view slides on http://localhost:8000

The content of slides is in **myslides.md** and all graphics are on **assets** folder. All customized styling goes to **assets/my_slides.css**.
