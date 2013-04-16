# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from wwod import common_crawl
reload(common_crawl)

# <codecell>

valid_segments = common_crawl.valid_segments()

# <codecell>

valid_segments[:5]

# <headingcell level=1>

# Run jobs

# <codecell>

jids = common_crawl.run_jobs(valid_segments, local=False)

# <codecell>

jids

# <codecell>

common_crawl.print_iresults(jids,local=False)

# <codecell>

r = common_crawl.tally_results(jids,local=False)

# <codecell>

r['count'], r['size'], r['runtime'], r['cost']

# <codecell>

plot(r["cores_vs_time_x"], r["cores_vs_time_y"])

# <codecell>


