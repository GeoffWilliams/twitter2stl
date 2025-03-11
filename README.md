# twitter2stl

3D Printed tweets!

This is just a quick and dirty python script for downloading a tweet and then rendering it to an STL file. Nothing serious, just for fun.


## WARNING

This project uses [twikit](https://github.com/d60/twikit) and using this library on twitter, even just to download a tweet will likely [result in getting banned](https://github.com/d60/twikit/issues?q=is%3Aissue%20state%3Aopen%20banned) - I lost a 7 year old account because of this.


## Setup
```shell
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt 

sudo apt -y install fonts-roboto openscad
```

Add twitter credentials as environment variables or use a [`.env` file](https://pypi.org/project/python-dotenv/). Example

```shell
TWITTER_USERNAME=someusername
TWITTER_EMAIL=someuser@megacorp.com
TWITTER_PASSWORD=hunter22
```

## How to use

1. Download a tweet from twitter: `tweet.py`
2. Render tweet to STL file: `3d.py`
3. Load STL file into slicer and print on 3D printer

**Twitter download script is disabled to avoid locking you out of twitter**

You can just edit `tweet.json` and run `3d.py` if you still want to try generating an STL

## Example files:
* `tweet_plaque.scad` - Rendered [OpenSCAD](https://openscad.org/) source codes
* `tweet_plaque.stl` - Rendered object, ready for printing

Have lots of fun!
