# phishing_app/views.py

from django.http import JsonResponse
from django.shortcuts import render
from .phishing_checker import (
    UsingIp,
    shortUrl,
    symbol,
    redirecting,
    SubDomains,
    DomainRegLen,
    RequestURL,
    AnchorURL,
    LinksInScriptTags,
    ServerFormHandler,
    InfoEmail,
    AbnormalURL,
    WebsiteForwarding,
    StatusBarCust,
    DisableRightClick,
    UsingPopupWindow,
    IframeRedirection,
    AgeofDomain,
    DNSRecording,
    WebsiteTraffic,
    PageRank,
    GoogleIndex,
    prefixSuffix,
    LinksPointingToPage,
    StatsReport,
)


def check_phishing(request):
    if request.method == "POST":
        url = request.POST.get("url")
        if url:
            using_ip_result = UsingIp(url)
            short_url_result = shortUrl(url)
            symbol_result = symbol(url)
            redirecting_result = redirecting(url)
            sub_domains_result = SubDomains(url)
            domain_reg_len_result = DomainRegLen(url)
            request_url_result = RequestURL(url)
            anchor_url_result = AnchorURL(url)
            links_in_script_tags_result = LinksInScriptTags(url)
            server_form_handler_result = ServerFormHandler(url)
            info_email_result = InfoEmail(url)
            abnormal_url_result = AbnormalURL(url)
            website_forwarding_result = WebsiteForwarding(url)
            status_bar_cust_result = StatusBarCust(url)
            disable_right_click_result = DisableRightClick(url)
            using_popup_window_result = UsingPopupWindow(url)
            iframe_redirection_result = IframeRedirection(url)
            age_of_domain_result = AgeofDomain(url)
            dns_recording_result = DNSRecording(url)
            website_traffic_result = WebsiteTraffic(url)
            page_rank_result = PageRank(url)
            google_index_result = GoogleIndex(url)
            prefix_suffix_result = prefixSuffix(url)
            links_pointing_to_page_result = LinksPointingToPage(url)
            stats_report_result = StatsReport(url)

            # Implement your phishing check logic here
            # You can combine and analyze the results as needed

            # Calculate an overall score based on the results
            overall_result = (
                using_ip_result
                + short_url_result
                + symbol_result
                + redirecting_result
                + sub_domains_result
                + domain_reg_len_result
                + request_url_result
                + anchor_url_result
                + links_in_script_tags_result
                + server_form_handler_result
                + info_email_result
                + abnormal_url_result
                + website_forwarding_result
                + status_bar_cust_result
                + disable_right_click_result
                + using_popup_window_result
                + iframe_redirection_result
                + age_of_domain_result
                + dns_recording_result
                + website_traffic_result
                + page_rank_result
                + google_index_result
                + prefix_suffix_result
                + links_pointing_to_page_result
                + stats_report_result
            )

            # Determine whether it's a phishing site based on your logic
            if overall_result < 0:
                result = "Phishing"
            else:
                result = "Safe"

            return JsonResponse({"result": result})
    else:
        return JsonResponse(
            {"error": "Request Invalid"},
            status=400,
        )


# def helloname(request):
#     return render(request, 'check_phishing.html')
