from upload.models import File, Collection
from upload.forms import handle_file
# https://github.com/fmalina/emails
from emails import send
from emails.imap_recipes import EMAIL_RE, get_user


def email_upload(msg, col_model=Collection):
    """
    Support uploads by email
    ------------------------
    Some user devices don't support web uploads such as mobile phones.
    Prompt these users to simply email photos to an email address for upload.
    Phones have a built in "email photo" utility, so no app download is needed.
    Attachments are processed extracting JPEG images.
    Extracted JPEG is added to the last updated collection of a user
        with the same email as the sender.
    Confirmation of successful upload sent just in case the email was spoofed.
    As this is not an iOS app, uploads will also work for devices such as
        Nokia S40 and S60 devices.

    Gmail filter:
        to:(upload email)
        ...label "Process/Uploads"
    """
    alt_stopwords = '.jpg .jpeg .png img image photo screenshot - _ \
                    0 1 2 3 4 5 6 7 8 9'.split()
    if not msg.is_multipart():
        return 'No attachement.'
    try:
        sender = EMAIL_RE.findall(msg["From"])[0]
    except IndexError:
        return 'No sender.'
    user = get_user(sender)
    if not user:
        return 'Sender is not a registered user.'
    col = col_model.objects.filter(user=user).last()
    if not col:
        return 'User has no listing/photo collection.'
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        data = part.get_payload(decode=True)
        fn = part.get_filename()
        fn = fn[:60] if fn else ''
        f = File(content_object=col, fn=fn)
        f.alt = f.fn.lower()
        for r in alt_stopwords:
            f.alt = f.alt.replace(r, '')
        f.save()
        y = handle_file(data, f)
        if y:
            send.email(user, 'Picture uploaded', 'uploaded', {'col': col, 'img': f})
            col.save()
        else:
            f.delete()
    return 'Done.'
