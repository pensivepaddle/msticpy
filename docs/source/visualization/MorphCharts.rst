Morph Charts
============

:py:mod:`msticpy.vis.morph_charts`

This module formats data and configuration files for use with http://morphcharts.com/.
In addition it renders http://morphcharts.com/ in an IFrame within the interface to allow
you to generate and interact with the charts generated by the data and configuration
files produced. This module is intended to be used in a Notebook environment.

This module uses templated Azure Sentinel KQL queries and templated chart configurations
included within MSTICpy.

Finding Charts
--------------
There are several ways to find what charts and queries are available for you to use.
list_charts() returns a list of all available charts:

.. code:: ipython3

    from msticpy.vis.morph_charts import MorphCharts
    morph = MorphCharts()
    morph.list_charts()

You can also use search_charts() to find charts that match a keyword search:

.. code:: ipython3

    morph.search_charts("Azure")

Once you have found a chart you wish to plot you can get further details with
get_chart_details(chart_name). This will show the description of the plot as
well as the name of the associated KQL query.

The queries can be found under the data source containers and are prefixed with
'morph'. These queries are called in the same way other queries are:

.. code:: ipython3

    query_provider.Azure.list_all_signins_geo(start=datetime(2020,4,8), end=datetime(2020,4,10))

Formatting and Rendering
------------------------
Once you have found the chart you wish to render and have the associated data you can
call display() and pass it the data, and chart name:

.. code:: ipython3

    morph.display(data=query_data, chart_name="SigninsChart")

This will format the data and chart configuration file and put them in a direcory named
'morphchart_package' in the current working directory. It will also return an IFrame
displaying http://morphcharts.com/. To load the charts within the IFrame click
"Choose Files" under "Load Package" heading. Select the 'description.json' and
'query_data.csv' files under the 'morphchart_package' folder to load the customised charts.

Creating New Chart Templates
----------------------------
You can create a add new chart templates for use by this module. The best way to do this
is by creating a customized chart set using http://morphcharts.com/designer.html. Once complete
save the chart, which will download a filed called 'description.json'. To add this as a template
by creating a YAML file with the following format:

.. code:: yaml

    Name: <The name of your chart>
    Description: <A description>
    Query: <The name of the query associated with your chart>
    Tags: <A list of keywords scribing the chart>
    DescriptionFile: <The JSON blob from your description.json file>

Then include the file in the msticpy/data/morph_charts folder and it will be discovered next time you
intialize an MorphCharts object.
