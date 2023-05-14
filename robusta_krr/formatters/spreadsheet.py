from __future__ import annotations

from robusta_krr.core.abstract.formatters import BaseFormatter
from robusta_krr.core.models.result import Result
import csv
import json
import pandas as pd
from io import StringIO

class SpreadSheetFormatter(BaseFormatter):
    """Formatter for spreadsheet output."""

    __display_name__ = "spreadsheet"

    
    def format(self, result: Result) -> str:
        """Format the result as spreadsheet

        :param result: The results to format.
        :type result: :class:`core.result.Result`
        :returns: The formatted results.
        :rtype: str
        """

        # Create empty lists to hold the data
        clusters = []
        names = []
        containers = []
        pods = []
        namespaces = []
        kinds = []
        request_cpus = []
        request_mems = []
        limit_cpus = []
        limit_mems = []
        severities = []

        json_data = json.loads(result.json())
        for scan in json_data['scans']: 
            clusters.append(scan['object']['cluster'])
            names.append(scan['object']['name'])
            containers.append(scan['object']['container'])
            pods.append(len(scan['object']['pods']))
            namespaces.append(scan['object']['namespace'])
            kinds.append(scan['object']['kind'])
            request_cpus.append(f"{scan['object']['allocations']['requests']['cpu']} -> {scan['recommended']['requests']['cpu']['value']}")
            request_mems.append(f"{scan['object']['allocations']['requests']['memory']} -> {scan['recommended']['requests']['memory']['value']}")
            limit_cpus.append(f"{scan['object']['allocations']['limits']['cpu']} -> {scan['recommended']['limits']['cpu']['value']}")
            limit_mems.append(f"{scan['object']['allocations']['limits']['memory']} -> {scan['recommended']['limits']['memory']['value']}")
            severities.append(scan['severity'])

        # Create a DataFrame with the extracted data
        df = pd.DataFrame({
            'Cluster': clusters,
            'Namespace': namespaces,
            'Name': names,
            'Pods': pods,
            'Type': kinds,
            'Container': containers,
            'CPU Requests': request_cpus,
            'CPU Limits': limit_cpus,
            'Memory Requests': request_mems,
            'Memory Limits': limit_mems,
            'Severity': severities
        })


        output = StringIO()
        df.to_csv(output, index=False, sep=',' , header=True)
        return output.getvalue()