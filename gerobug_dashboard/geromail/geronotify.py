import requests
import json
import logging
from prerequisites.models import Webhook



def notify_slack(title, hunter, action):
    try:
        webhook = Webhook.objects.get(webhook_service="SLACK").webhook_handle # SLACK WEBHOOK
        if action == "NEW_REPORT":
            payload = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "\n*:warning: NEW REPORT RECEIVED :warning:*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Title = *"+title+"*\nReporter = *"+hunter+"*"
                        }
                    }
                ]
            }
        elif action == "NEW_UPDATE":
            payload = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "\n*:warning: NEW UPDATE/AMEND RECEIVED :warning:*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Report ID = *"+title+"*\nReporter = *"+hunter+"*"
                        }
                    }
                ]
            }
        elif action == "NEW_APPEAL":
            payload = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "\n*:warning: NEW APPEAL RECEIVED :warning:*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Report ID = *"+title+"*\nReporter = *"+hunter+"*"
                        }
                    }
                ]
            }
        elif action == "NEW_AGREE":
            payload = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "\n*:warning: HUNTER AGREEMENT RECEIVED :warning:*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Report ID = *"+title+"*\nReporter = *"+hunter+"*\nReport will be automatically moved to the next phase."
                        }
                    }
                ]
            }
        elif action == "NEW_NDA":
            payload = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "\n*:warning: NEW NDA SUBMISSION RECEIVED :warning:*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Report ID = *"+title+"*\nReporter = *"+hunter+"*"
                        }
                    }
                ]
            }

        logging.getLogger("Gerologger").debug(f"Sending Slack notification: {action} - {title}")
        response = requests.post(webhook, json.dumps(payload), timeout=10)
        response.raise_for_status()
        logging.getLogger("Gerologger").debug("Slack notification sent successfully")
        return True

    except requests.exceptions.Timeout:
        logging.getLogger("Gerologger").error(f"Slack webhook timeout (10s): {action} - {title}")
        return False
    except requests.exceptions.RequestException as e:
        logging.getLogger("Gerologger").error(f"Slack webhook failed: {type(e).__name__}: {e}")
        return False
    except Exception as e:
        logging.getLogger("Gerologger").error(f"Slack notification error: {type(e).__name__}: {e}")
        return False

def notify_telegram(title, hunter, action):
    try:
        # webhook = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}"
        webhook = Webhook.objects.get(webhook_service="TELEGRAM").webhook_handle # TELEGRAM WEBHOOK
        if action == "NEW_REPORT":
            message = \
"*🚨 NEW REPORT RECEIVED 🚨*\n\
=========================\n\
Title        = *"+title+"*\n\
Reporter = *"+hunter+"*"\

        elif action == "NEW_UPDATE":
            message = "\n\
*🚨 NEW UPDATE/AMEND RECEIVED 🚨*\n\
=========================\n\
Report ID = *"+title+"*\n\
Reporter  = *"+hunter+"*"\
        
        elif action == "NEW_APPEAL":
            message = "\n\
*🚨 NEW APPEAL RECEIVED 🚨*\n\
=========================\n\
Report ID = *"+title+"*\n\
Reporter  = *"+hunter+"*"\
        
        elif action == "NEW_AGREE":
            message = "\n\
*🚨 HUNTER AGREEMENT RECEIVED 🚨*\n\
=========================\n\
Report ID = *"+title+"*\n\
Reporter  = *"+hunter+"*\n\
Report will be automatically moved to the next phase."
        
        elif action == "NEW_NDA":
            message = "\n\
*🚨 NEW NDA SUBMISSION RECEIVED 🚨*\n\
=========================\n\
Report ID = *"+title+"*\n\
Reporter  = *"+hunter+"*"\

        webhook = webhook+"&parse_mode=Markdown&text="+message
        
        logging.getLogger("Gerologger").debug(f"Sending Telegram notification: {action} - {title}")
        response = requests.get(webhook, timeout=10)
        response.raise_for_status()
        logging.getLogger("Gerologger").debug("Telegram notification sent successfully")
        return True

    except requests.exceptions.Timeout:
        logging.getLogger("Gerologger").error(f"Telegram webhook timeout (10s): {action} - {title}")
        return False
    except requests.exceptions.RequestException as e:
        logging.getLogger("Gerologger").error(f"Telegram webhook failed: {type(e).__name__}: {e}")
        return False
    except Exception as e:
        logging.getLogger("Gerologger").error(f"Telegram notification error: {type(e).__name__}: {e}")
        return False

def notify(title, hunter, action):
    results = []
    
    if Webhook.objects.filter(webhook_service="SLACK").exists():
        success = notify_slack(title, hunter, action)
        results.append(success)

    if Webhook.objects.filter(webhook_service="TELEGRAM").exists():
        success = notify_telegram(title, hunter, action)
        results.append(success)
    
    return any(results) if results else True
