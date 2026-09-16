"""
HTML reporter — generates a standalone HTML test report.
"""
import os
from datetime import datetime, timezone
from framework.core.test_result import TestResult, SuiteResult, TestStatus

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<title>Test Report - {{ suite_name }}</title>
<style>
body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
.header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }
.summary { display: flex; gap: 20px; margin: 20px 0; }
.stat-card { background: white; padding: 15px; border-radius: 8px; text-align: center;
             box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex: 1; }
.stat-card h2 { margin: 0; font-size: 2em; }
.pass { color: #27ae60; } .fail { color: #e74c3c; }
.error { color: #e67e22; } .skip { color: #95a5a6; }
table { width: 100%; border-collapse: collapse; background: white;
        border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
th { background: #34495e; color: white; padding: 12px; text-align: left; }
td { padding: 10px 12px; border-bottom: 1px solid #eee; }
tr:hover { background: #f8f9fa; }
.status-pass { color: #27ae60; font-weight: bold; }
.status-fail { color: #e74c3c; font-weight: bold; }
.status-error { color: #e67e22; font-weight: bold; }
.status-skip { color: #95a5a6; }
.error-msg { font-size: 0.85em; color: #666; margin-top: 4px; }
</style>
</head>
<body>
<div class="header">
<h1>Test Report</h1>
<p>Suite: {{ suite_name }} | Generated: {{ timestamp }}</p>
</div>
<div class="summary">
<div class="stat-card"><h2 class="pass">{{ passed }}</h2><p>Passed</p></div>
<div class="stat-card"><h2 class="fail">{{ failed }}</h2><p>Failed</p></div>
<div class="stat-card"><h2 class="error">{{ errors }}</h2><p>Errors</p></div>
<div class="stat-card"><h2 class="skip">{{ skipped }}</h2><p>Skipped</p></div>
<div class="stat-card"><h2>{{ pass_rate }}%</h2><p>Pass Rate</p></div>
<div class="stat-card"><h2>{{ duration }}s</h2><p>Duration</p></div>
</div>
<table>
<tr><th>Test Name</th><th>Status</th><th>Duration</th><th>Details</th></tr>
{{ rows }}
</table>
</body></html>"""


class HTMLReporter:
    def __init__(self, output_path: str = "reports/test_report.html"):
        self.output_path = output_path

    def on_suite_start(self, suite_name: str):
        pass

    def on_test_result(self, result: TestResult):
        pass

    def on_suite_end(self, suite_result: SuiteResult):
        rows = ""
        for r in suite_result.results:
            status_class = f"status-{r.status.value.lower()}"
            detail = ""
            if r.error_message:
                safe_msg = r.error_message.replace("<", "&​lt;").replace(">", "&​gt;")
                detail = f'<div class="error-msg">{safe_msg}</div>'
            if r.retry_count > 0:
                detail += f'<div class="error-msg">Retry #{r.retry_count}</div>'

            rows += (f'<tr><td>{r.test_name}</td>'
                     f'<td class="{status_class}">{r.status.value}</td>'
                     f'<td>{r.duration_sec:.3f}s</td>'
                     f'<td>{detail}</td></tr>\n')

        html = (HTML_TEMPLATE
                .replace("{{ suite_name }}", suite_result.suite_name)
                .replace("{{ timestamp }}", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
                .replace("{{ passed }}", str(suite_result.passed))
                .replace("{{ failed }}", str(suite_result.failed))
                .replace("{{ errors }}", str(suite_result.errors))
                .replace("{{ skipped }}", str(suite_result.skipped))
                .replace("{{ pass_rate }}", f"{suite_result.pass_rate:.1f}")
                .replace("{{ duration }}", f"{suite_result.duration_sec:.3f}")
                .replace("{{ rows }}", rows))

        os.makedirs(os.path.dirname(self.output_path) or ".", exist_ok=True)
        with open(self.output_path, "w") as f:
            f.write(html)
