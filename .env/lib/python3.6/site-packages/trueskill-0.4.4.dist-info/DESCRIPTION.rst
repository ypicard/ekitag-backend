
TrueSkill
~~~~~~~~~

An implementation of the TrueSkill algorithm for Python.  TrueSkill is a rating
system among game players and it is used on Xbox Live to rank and match
players.

.. sourcecode:: python

   from trueskill import Rating, quality_1vs1, rate_1vs1
   alice, bob = Rating(25), Rating(30)  # assign Alice and Bob's ratings
   if quality_1vs1(alice, bob) < 0.50:
       print('This match seems to be not so fair')
   alice, bob = rate_1vs1(alice, bob)  # update the ratings after the match

Links
`````

Documentation
   http://trueskill.org/
GitHub:
   http://github.com/sublee/trueskill
Mailing list:
   trueskill@librelist.com
List archive:
   http://librelist.com/browser/trueskill
Continuous integration (Travis CI)
   https://travis-ci.org/sublee/trueskill

   .. image:: https://api.travis-ci.org/sublee/trueskill.png

See Also
````````

- `TrueSkill(TM) Ranking System by Microsoft
  <http://research.microsoft.com/en-us/projects/trueskill/>`_
- `"Computing Your Skill" by Jeff Moser <http://bit.ly/moserware-trueskill>`_
- `"The Math Behind TrueSkill" by Jeff Moser <http://bit.ly/trueskill-math>`_
- `TrueSkill Calcurator by Microsoft
  <http://atom.research.microsoft.com/trueskill/rankcalculator.aspx>`_



