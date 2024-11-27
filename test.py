from lib.workbook_parser import Parse_Meeting_WorkBook
import aiohttp
import asyncio


def main():
    site_domain = 'https://www.jw.org'
    workbook_url = "https://www.jw.org/ro/biblioteca/caiet-pentru-intrunire/septembrie-octombrie-2024-mwb/"
    data_dict = None
    parser = Parse_Meeting_WorkBook(site_domain, workbook_url)

    try:
        data_dict = asyncio.run(parser.get_dict_data())
    except aiohttp.client_exceptions.InvalidURL:
        print("Info Download", "Error! Please enter correct lik in link tab.")
    except aiohttp.client_exceptions.ClientConnectorError:
        print("Info Download", "Connection Error! Please check your connection")

    print(data_dict)


if __name__ == "__main__":
    main()