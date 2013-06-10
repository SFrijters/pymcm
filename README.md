# pymcm-deckbox

pymcm-deckbox is a library for interacting with web https://www.magiccardmarket.eu/ and http://www.deckbox.org. It is based on pymcm.

## Requires

  * httplib2
  * mechanize
  * lxml

## Installation

```bash
pip install pymcm
```

If you install lxml from pip, will install the packages:

```bash
sudo apt-get install libxml2-dev libxslt-dev
```

## Usage

### Login and search card

```python
import pymcm-deckbox

mcm = MCMApi(username='foo', password='duu')

for result in mcm.search('sun titan'):
    print result.card.name, result.available
```

### Read want lists

```python
for wl in mcm.get_wants_list():
    print wl.name

    for want_card in wl.wants:
        print want_card.card.name, want_card.amount
```

### Read a card prices

```python
one_card = wl.wants[0].card

for pc in mcm.list_prices(one_card):
    print "{0} ({1}): {2} {3}".format(pc.seller.name, pc.seller.country, pc.condition, pc.price)
```

### Add a card to cart

```python
pc = mcm.list_prices(one_card)[0]
mcm.add_to_cart(pc)
```

### Read a cart

```python
cart = mcm.get_cart()

print cart.total()
for ship in cart.ships():
    print ship.seller.name
    for a in ship.articles:
        print a.card.name, a.price
```

### Calculate value of missing cards of a deck

```python
db = DeckboxApi(username='foo',password='foo',mcmUsername='',mcmPassword='')
db.login()
db.get_deck_needs('name of the deck')
```

## Contacts

The original pymcm is written by:

* Benito Rodriguez - brarcos@gmail.com

pymcm-deckbox extension is written by:

* Stefan Frijters - sfrijters@gmail.com

Suggestions, bugs,... https://github.com/SFrijters/pymcm/issues

