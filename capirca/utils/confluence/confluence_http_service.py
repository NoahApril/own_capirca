import requests
from requests.auth import HTTPBasicAuth
import json


class ConfluenceService:
    def __init__(self, base_url, username, api_token):
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
    def get_spaces(self, keys=None):
        url = f"{self.base_url}/rest/api/space"
        params = {}
        if keys:
            params['spaceKey'] = keys[0]

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(f"Failed to retrieve spaces. Status Code: {response.status_code} Response: {response.text}")

    def fetch_page_details(self, page_id):
        url =  f"{self.base_url}/rest/api/content/{page_id}"
        params = {"expand": "history,children.page,body.view,ancestors,version,descendants.page"}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

    def fetch_all_child_pages(self, page_id):
        all_pages = []
        start = 0
        limit = 25

        while True:
            url = f"{self.base_url}/rest/api/content/{page_id}/child/page"
            params = {"start": start, "limit": limit}
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = json.loads(response.text)
                all_pages.extend(data['results'])
                if 'next' in data['_links']:
                    start += limit
                else:
                    break
            else:
                raise Exception(f"Failed to retrieve child pages. Status Code: {response.status_code} Response: {response.text}")

        return all_pages


    def get_pages(self, space_ids=None, status=None, title=None, body_format=None, cursor=None, limit=25):
        url = f"{self.base_url}/rest/pages"
        params = {
            "spaceId": ','.join(map(str, space_ids)) if space_ids else None,
            "status": ','.join(status) if status else None,
            "title": title,
            "body-format": body_format,
            "cursor": cursor,
            "limit": limit
        }

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(f"Failed to retrieve pages. Status Code: {response.status_code} Response: {response.text}")

    def get_space_pages(self, space_id, sort=None, status=None, title=None, body_format=None, cursor=None,
                        limit=25):
        url = f"{self.base_url}/rest/api/spaces/{space_id}/pages"
        params = {
            "sort": sort,
            "status": ','.join(status) if status else None,
            "title": title,
            "body-format": body_format,
            "cursor": cursor,
            "limit": limit
        }

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(
                f"Failed to retrieve pages in space. Status Code: {response.status_code} Response: {response.text}")



    def export_pdf(self, page_id):
        """Export page as PDF using Confluence's flyingpdf action"""
        url = f"{self.base_url}/spaces/flyingpdf/pdfpageexport.action?pageId={page_id}"
        headers = {
            **self.headers,
            "Accept": "application/pdf",
            "Content-Type": "application/pdf",
            "X-Atlassian-Token": "no-check"
        }

        response = requests.get(url, headers=headers, allow_redirects=True)

        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                return response.content
            else:
                raise Exception(f"Received non-PDF response: {content_type}")
        else:
            raise Exception(f"Failed to export PDF. Status Code: {response.status_code} Response: {response.text}")

    def get_content_id_from_url(self, url_path):
        # Assuming the URL path is in the format '/display/SPACE_KEY/PAGE_TITLE'
        if 'pageId' in url_path:
            return url_path.split('=')[1]


        if '/x/' in url_path:
            # Fetch the page details using the shared link
            response = requests.head(url_path, headers=self.headers, allow_redirects=True)
            if response.status_code == 200:
                final_url = response.url
                url_path = final_url.replace('https://confluence.hrz.uni-bielefeld.de', '')
            else:
                print(
                    f"Failed to retrieve content ID from shared link {url_path}. Status Code: {response.status_code} Response: {response.text}")
                return None

        if '/pages/' in url_path:
            # the page Id is already present in the URL
            # example 'https://confluence.hrz.uni-bielefeld.de/spaces/BET/pages/83296344/vSphere-Cluster+GP'
            # get the page ID from the URL after /pages/
            index_pages = url_path.index('/pages/')
            url_path = url_path[index_pages:]
            # take the id after /pages/
            page_id = url_path.split('/')[2]
            return page_id

        if 'https://confluence.hrz.uni-bielefeld.de' in url_path:
            url_path = url_path.replace('https://confluence.hrz.uni-bielefeld.de', '')

        try:
            parts = url_path.split('/')
            if len(parts) == 6:
                page_title = parts[5]
            else:
                page_title = parts[3]
            space_key = parts[2]

            # Fetch the page details using the space key and page title
            url = f"{self.base_url}/rest/api/content"
            params = {
                "spaceKey": space_key,
                "title": page_title,
                "expand": "history,children.page,body.view,ancestors,version,descendants.page"
            }
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    return data['results'][0]['id']
            return None
        except Exception as e:
            # Log or save the problematic URL
            with open("problematic_urls.log", "a") as log_file:
                log_file.write(f"Problematic URL: {url_path}\nError: {str(e)}\n")
            print(f"Error processing URL: {url_path}. Logged to 'problematic_urls.log'.")
            return None

    def add_label_to_page(self, page_id, label):
        url = f"{self.base_url}/rest/api/content/{page_id}/label"
        data = {
            "prefix": "global",
            "name": label
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print(f"Label '{label}' added to page {page_id}")
        else:
            print(f"Failed to add label. Status Code: {response.status_code} Response: {response.text}")

    def remove_label_from_page(self, page_id, label):
        url = f"{self.base_url}/rest/api/content/{page_id}/label/{label}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            print(f"Label '{label}' removed from page {page_id}")
        else:
            print(f"Failed to remove label. Status Code: {response.status_code} Response: {response.text}")

    def get_labels(self, page_id):
        url = f"{self.base_url}/rest/api/content/{page_id}/label"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            labels = [label['name'] for label in response.json()['results']]
            return labels
        else:
            print(f"Failed to retrieve labels. Status Code: {response.status_code} Response: {response.text}")
            return []


    def get_attachments(self, page_id):
        """Get all attachments for a page"""
        url = f"{self.base_url}/rest/api/content/{page_id}/child/attachment"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['results']
        return None

    def download_attachment(self, attachment_data):
        """Download specific attachment content"""
        if '_links' in attachment_data and 'download' in attachment_data['_links']:
            download_url = f"{self.base_url}{attachment_data['_links']['download']}"
            response = requests.get(download_url, headers=self.headers)
            if response.status_code == 200:
                return response.content
        return None


    def search_pages_by_cql(self, cql_query,start, limit=250):
        url = f"{self.base_url}/rest/api/content/search"
        params = {
            "cql": cql_query,
            "start": start,
            "limit": limit
        }

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to search pages by CQL. Status Code: {response.status_code} Response: {response.text}")