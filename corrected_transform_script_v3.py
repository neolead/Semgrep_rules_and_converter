
import json
from bs4 import BeautifulSoup

def results_to_final_html(sorted_results):
    """Convert sorted results to the final HTML format."""
    soup = BeautifulSoup('', 'html.parser')

    # Add required CSS and JS for Bootstrap and DataTables
    html_tag = soup.new_tag("html")
    head_tag = soup.new_tag("head")
    html_tag.append(head_tag)
    soup.append(html_tag)

    link_tag = soup.new_tag("link", href="https://cdn.datatables.net/1.10.24/css/dataTables.bootstrap4.min.css", rel="stylesheet")
    head_tag.append(link_tag)
    link_tag = soup.new_tag("link", href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css", rel="stylesheet")
    head_tag.append(link_tag)

    body_tag = soup.new_tag("body", **{"class": "bg-dark text-white"})
    html_tag.append(body_tag)

    container = soup.new_tag("div", **{"class": "container-fluid mt-5 pl-1"})
    body_tag.append(container)

    table = soup.new_tag("table", **{"class": "table table-dark table-striped table-bordered", "id": "resultsTable"})
    container.append(table)

    thead = soup.new_tag("thead")
    table.append(thead)

    headers = ["Path", "Check ID", "Severity", "Message", "Link"]
    tr = soup.new_tag("tr")
    for header in headers:
        th = soup.new_tag("th")
        th.string = header
        tr.append(th)
    thead.append(tr)

    tbody = soup.new_tag("tbody")
    table.append(tbody)

    for result in sorted_results:
        tr = soup.new_tag("tr")
        for key in ['path', 'check_id', 'extra']:
            td = soup.new_tag("td")
            if key == 'extra':
                td.string = result[key]['severity']
            else:
                td.string = result[key]
            tr.append(td)
        td = soup.new_tag("td")
        td.string = result['extra']['message']
        tr.append(td)
        td = soup.new_tag("td")
        shortlink = result['extra']['metadata'].get('shortlink', '#')
        a_tag = soup.new_tag("a", href=shortlink)
        a_tag.string = "Link"
        td.append(a_tag)
        tr.append(td)
        tbody.append(tr)

    # Adding JS for Bootstrap and DataTables
    scripts = [
        "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js",
        "https://cdn.datatables.net/1.10.24/js/dataTables.bootstrap4.min.js",
        "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
    ]
    for script in scripts:
        script_tag = soup.new_tag("script", src=script)
        body_tag.append(script_tag)

    # Activate DataTables with the given display length
    script_tag = soup.new_tag("script")
    script_tag.string = "$(document).ready(function() { $('#resultsTable').DataTable({ 'displayLength': 150 }); } );"
    body_tag.append(script_tag)

    return str(soup)


def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <input_json> <output_html>")
        sys.exit(1)

    input_json_path = sys.argv[1]
    output_html_path = sys.argv[2]

    with open(input_json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    if isinstance(data, dict) and 'results' in data:
        data = data['results']

    sorted_results = sorted(data, key=lambda x: x['extra']['severity'])
    html_content = results_to_final_html(sorted_results)

    with open(output_html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)


if __name__ == "__main__":
    main()
