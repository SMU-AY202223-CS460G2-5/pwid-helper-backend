# Constants for FlashID
class Message:
    ONBOARD_SUCCESS = (
        "Thank you {} for signing up with FlashID.\nWe appreciate your time to "
        "contribute to the society and your help will greatly help the PWID."
    )
    START_BOT_USER_ALREADY_EXIST = "You already started the bot."
    PWID_REQUEST = "Help has been called. Please hold on tight."
    BROADCAST_REQUEST = (
        "<strong>⚠️Help Requested‼️</strong>\nA PWID has called for help at:"
        "\nLocation: {}\nPWID ID: {}"
    )
    ACCEPTED_REQUEST = (
        "Thank you for accepting this request.\n More information will  be provided "
        "below.\nName: {}\nCaregiver Contact Number: {}\nnLocation: {} \nDisabilities: "
        "{}\nPlease show your diagram to the PWID for verification."
    )
    PWID_RESPONSE = (
        "Do not worry. Help is on the way.\nPlease see your microbit for the same "
        "diagram to show your helper."
    )
    BROADCAST_ACCEPTED = (
        "Thank you everyone, this request has been taken and help is already on the way"
    )
    GENDER_REQUEST = (
        "Before lending a hand, please let us know the preferred gender you wish to "
        "help."
    )
    LANGUAGE_POLL_QUESTION = "Please select your preferred language."
