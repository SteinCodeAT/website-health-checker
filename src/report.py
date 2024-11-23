""" This module holds the main report creator class. It is responsible for creating the html report file with the results of the health check. """
from typing import List
from pathlib import Path
from datetime import datetime

from loguru import logger

from src.data_objects import LinkRecord


class HtmlReportPrinter:

    def __init__(self):
        # Paths
        self.root_path = Path(__file__).parent.parent
        self.output_path = self.root_path.joinpath("reports")

    def create_link_record_html(self, record: LinkRecord, record_type: str):
        """ Creates the standard html for a single link record. They are identical for each list 
        and customized using the record_type css class
        :param record: LinkRecord
        :param record_type: str - css class to apply to the record div. Can be "success", "warning" or "error"
        """
        link_record_html =  f"""
            <div class="record {record_type}">
                <div class="record-link-wrapper">
                    <a class="record-link" href="{record.link}" target="_blank">{record.link}</a>
                    <div class="found-in-link-wrapper"><span>Found in:</span> 
        """

        for found_in_page in set(record.found_in_page):
            link_record_html += f'<a class="found-in-link" href="{found_in_page}" target="_blank">{found_in_page}</a>'

        link_record_html += f"""
                    </div>
                </div>
                <div class="record_meta">
                    <span>Type: {record.resource_type.value}</span><span>Status: {record.status_code}</span>
                </div>
            </div>
        """

        return link_record_html
    
    def print_report(self, broken_links: List[LinkRecord], redirected_links: List[LinkRecord], working_links: List[LinkRecord]):
        """ Prints the report to an html file in the output directory in the root of the project """
        logger.info("Creating Report html file...")

        now = datetime.now()
        date_time_short_label = now.strftime("%Y%m%d-%H%M")
        date_time_long_label = now.strftime("%Y-%m-%d %H:%M")

        if not self.output_path.exists():
            self.output_path.mkdir()

        file_name = self.output_path.joinpath(f"{date_time_short_label}_health_check_report.html")
        
        logger.info(f"Writing report to file: {file_name}")

        with open(file_name, "w") as file:
            file.write(f"""
                <html>
                       <head>
                            <title>Health Check Report {date_time_long_label}</title>
                            <style>
                                body {{ 
                                    font-size: 14px; font-family: Arial, sans-serif; 
                                    background-color: #f5f5f5;
                                    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 304 304' width='304' height='304'%3E%3Cpath fill='%23ce98c9' fill-opacity='0.1' d='M44.1 224a5 5 0 1 1 0 2H0v-2h44.1zm160 48a5 5 0 1 1 0 2H82v-2h122.1zm57.8-46a5 5 0 1 1 0-2H304v2h-42.1zm0 16a5 5 0 1 1 0-2H304v2h-42.1zm6.2-114a5 5 0 1 1 0 2h-86.2a5 5 0 1 1 0-2h86.2zm-256-48a5 5 0 1 1 0 2H0v-2h12.1zm185.8 34a5 5 0 1 1 0-2h86.2a5 5 0 1 1 0 2h-86.2zM258 12.1a5 5 0 1 1-2 0V0h2v12.1zm-64 208a5 5 0 1 1-2 0v-54.2a5 5 0 1 1 2 0v54.2zm48-198.2V80h62v2h-64V21.9a5 5 0 1 1 2 0zm16 16V64h46v2h-48V37.9a5 5 0 1 1 2 0zm-128 96V208h16v12.1a5 5 0 1 1-2 0V210h-16v-76.1a5 5 0 1 1 2 0zm-5.9-21.9a5 5 0 1 1 0 2H114v48H85.9a5 5 0 1 1 0-2H112v-48h12.1zm-6.2 130a5 5 0 1 1 0-2H176v-74.1a5 5 0 1 1 2 0V242h-60.1zm-16-64a5 5 0 1 1 0-2H114v48h10.1a5 5 0 1 1 0 2H112v-48h-10.1zM66 284.1a5 5 0 1 1-2 0V274H50v30h-2v-32h18v12.1zM236.1 176a5 5 0 1 1 0 2H226v94h48v32h-2v-30h-48v-98h12.1zm25.8-30a5 5 0 1 1 0-2H274v44.1a5 5 0 1 1-2 0V146h-10.1zm-64 96a5 5 0 1 1 0-2H208v-80h16v-14h-42.1a5 5 0 1 1 0-2H226v18h-16v80h-12.1zm86.2-210a5 5 0 1 1 0 2H272V0h2v32h10.1zM98 101.9V146H53.9a5 5 0 1 1 0-2H96v-42.1a5 5 0 1 1 2 0zM53.9 34a5 5 0 1 1 0-2H80V0h2v34H53.9zm60.1 3.9V66H82v64H69.9a5 5 0 1 1 0-2H80V64h32V37.9a5 5 0 1 1 2 0zM101.9 82a5 5 0 1 1 0-2H128V37.9a5 5 0 1 1 2 0V82h-28.1zm16-64a5 5 0 1 1 0-2H146v44.1a5 5 0 1 1-2 0V18h-26.1zm102.2 270a5 5 0 1 1 0 2H98v14h-2v-16h124.1zM242 149.9V160h16v34h-16v62h48v48h-2v-46h-48v-66h16v-30h-16v-12.1a5 5 0 1 1 2 0zM53.9 18a5 5 0 1 1 0-2H64V2H48V0h18v18H53.9zm112 32a5 5 0 1 1 0-2H192V0h50v2h-48v48h-28.1zm-48-48a5 5 0 0 1-9.8-2h2.07a3 3 0 1 0 5.66 0H178v34h-18V21.9a5 5 0 1 1 2 0V32h14V2h-58.1zm0 96a5 5 0 1 1 0-2H137l32-32h39V21.9a5 5 0 1 1 2 0V66h-40.17l-32 32H117.9zm28.1 90.1a5 5 0 1 1-2 0v-76.51L175.59 80H224V21.9a5 5 0 1 1 2 0V82h-49.59L146 112.41v75.69zm16 32a5 5 0 1 1-2 0v-99.51L184.59 96H300.1a5 5 0 0 1 3.9-3.9v2.07a3 3 0 0 0 0 5.66v2.07a5 5 0 0 1-3.9-3.9H185.41L162 121.41v98.69zm-144-64a5 5 0 1 1-2 0v-3.51l48-48V48h32V0h2v50H66v55.41l-48 48v2.69zM50 53.9v43.51l-48 48V208h26.1a5 5 0 1 1 0 2H0v-65.41l48-48V53.9a5 5 0 1 1 2 0zm-16 16V89.41l-34 34v-2.82l32-32V69.9a5 5 0 1 1 2 0zM12.1 32a5 5 0 1 1 0 2H9.41L0 43.41V40.6L8.59 32h3.51zm265.8 18a5 5 0 1 1 0-2h18.69l7.41-7.41v2.82L297.41 50H277.9zm-16 160a5 5 0 1 1 0-2H288v-71.41l16-16v2.82l-14 14V210h-28.1zm-208 32a5 5 0 1 1 0-2H64v-22.59L40.59 194H21.9a5 5 0 1 1 0-2H41.41L66 216.59V242H53.9zm150.2 14a5 5 0 1 1 0 2H96v-56.6L56.6 162H37.9a5 5 0 1 1 0-2h19.5L98 200.6V256h106.1zm-150.2 2a5 5 0 1 1 0-2H80v-46.59L48.59 178H21.9a5 5 0 1 1 0-2H49.41L82 208.59V258H53.9zM34 39.8v1.61L9.41 66H0v-2h8.59L32 40.59V0h2v39.8zM2 300.1a5 5 0 0 1 3.9 3.9H3.83A3 3 0 0 0 0 302.17V256h18v48h-2v-46H2v42.1zM34 241v63h-2v-62H0v-2h34v1zM17 18H0v-2h16V0h2v18h-1zm273-2h14v2h-16V0h2v16zm-32 273v15h-2v-14h-14v14h-2v-16h18v1zM0 92.1A5.02 5.02 0 0 1 6 97a5 5 0 0 1-6 4.9v-2.07a3 3 0 1 0 0-5.66V92.1zM80 272h2v32h-2v-32zm37.9 32h-2.07a3 3 0 0 0-5.66 0h-2.07a5 5 0 0 1 9.8 0zM5.9 0A5.02 5.02 0 0 1 0 5.9V3.83A3 3 0 0 0 3.83 0H5.9zm294.2 0h2.07A3 3 0 0 0 304 3.83V5.9a5 5 0 0 1-3.9-5.9zm3.9 300.1v2.07a3 3 0 0 0-1.83 1.83h-2.07a5 5 0 0 1 3.9-3.9zM97 100a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-48 32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 48a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-64a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 96a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-144a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-96 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm96 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-64a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-32 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM49 36a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-32 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM33 68a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-48a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 240a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-64a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm80-176a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 48a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm112 176a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM17 180a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM17 84a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 64a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6z'%3E%3C/path%3E%3C/svg%3E");
                                }}
                                main {{ 
                                    max-width: 800px; margin: 0 auto; padding: 1.5rem; 
                                    background-color: white; box-shadow: 4px 4px 4px rgba(0,0,0,0.2); border: 1px solid rgba(0,0,0,0.1);
                                }}
                                h1 {{ margin-bottom: 0}}
                                h2 {{ margin-top: 2rem}}

                                .summary {{ margin-bottom: 1rem}}
                                .summary-wrapper {{ display: grid; gap: 1rem; grid-template-columns: 1fr 1fr 1fr 1fr; }}
                                .summary-item {{ display: flex; flex-direction: column; text-decoration: none; align-items: center; justify-content: center; gap: 0.2rem; transition: filter 0.3s; }}
                                .summary-item:hover {{ filter: brightness(1.5); }}
                                .summary-item--highlight {{ font-size: 2rem; font-weight: bold; color: #303030;}}
                                .summary-item small {{ color: #303030; font-size: 0.8rem;}}

                                .record-wrapper {{ display: flex; flex-direction:column}}

                                .record {{ display: flex; flex-direction: row; gap: 0.5rem; padding: 1rem; border: 1px solid #ccc; 
                                border-radius: 5px; margin-bottom: 1rem; justify-content: space-between; }}

                                .record.success {{ border-left: 5px solid green; }}
                                .record.warning {{ border-left: 5px solid orange; }}
                                .record.error {{ border-left: 5px solid red; }}
                                .record-link {{ color: #303030; font-weight: bold; transition: filter 0.3s; font-size: 110%;}}

                                .found-in-link-wrapper {{ display: flex; flex-direction: column; gap: 0.1rem; font-size: 0.8rem; color: #303030; margin-top: 0.5rem }}
                                .found-in-link {{ color: #303030; transition: filter 0.3s; }}
                                .found-in-link:hover,.record-link:hover {{ filter: brightness(1.5); }}
                                
                                .record-link-wrapper {{display: flex, flex-direction: column;}}
                                
                                .record-content {{ display: flex; gap: 0.5rem; justify-content: space-between; }}
                                .record_meta {{ display: flex; flex-direction: column; gap: 0.2rem; font-size: 0.8rem; color: #666; white-space: nowrap }}
                            </style>
                        </head>
                    <body>
                        <main>
                            <h1>Health Check Report</h1>
                            <small>Generated at: {date_time_long_label}</small>

                            <div class="summary">
                                <h2>Summary</h2>

                                <div class="summary-wrapper">
                                    <a href="#" class="summary-item">
                                        <span class="summary-item--highlight">{len(working_links + redirected_links + broken_links)}</span>
                                        <small>Total Links</small>
                                    </a>
                                    <a href="#broken-links" class="summary-item">
                                        <span class="summary-item--highlight">{len(broken_links)}</span>
                                        <small>Broken Links</small>
                                    </a>
                                    <a href="#redirected-links" class="summary-item">
                                        <span class="summary-item--highlight">{len(redirected_links)}</span>
                                        <small>Redirected Links</small>
                                    </a>
                                    <a href="#working-links" class="summary-item">
                                        <span class="summary-item--highlight">{len(working_links)}</span>
                                        <small>Working Links</small>
                                    </a>
                                </div>                                
                            </div>

                            <h2 id="#broken-links">Broken Links - {len(broken_links)}</h2>

                            <div class="record-wrapper">
            """)

            for record in broken_links:
                file.write(self.create_link_record_html(record, "error"))

            file.write("</div>")

            file.write(f"""
                       <h2 id="#redirected-links" >Redirected Links - {len(redirected_links)}</h2>
                       <div class="record-wrapper">
            """)

            
            for record in redirected_links:
                file.write(self.create_link_record_html(record, "warning"))
                
            file.write("</div>")

            file.write(f"""
                       <h2 id="working-links">Working Links - {len(working_links)}</h2>
                       <div class="record-wrapper">
            """)

            
            for record in working_links:
                file.write(self.create_link_record_html(record, "success"))

            file.write("""
                        </div>
                       </main>
                    </body>
                </html>
            """)
