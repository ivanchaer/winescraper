wine_template = """
<wine id="$wine_id" url="$wine_url">
    $wine_data
</wine>
"""

row_template = """
<$field_label>
<![CDATA[
$field_content
]]>
</$field_label>
    """