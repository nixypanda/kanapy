This document provides a mental model for understanding the Kayako API and its various resources.

/api/v1/
    users/
        <id>/
            activities (GET)
            cases (GET)
        fields/ (GET|POST|DELETE)
            <id>/ (GET|PUT|DELETE)
                options/ (DELETE)
                    <id>/ (DELETE)
                    reorder (PUT)
                values (GET)
            reorder (PUT)


    identities/
        email/ (GET|POST|DELETE)
            <id>/ (GET|PUT|DELETE)
                send_verification_email (PUT)

        phones/ (GET|POST|DELETE)
            <id>/ (GET|PUT|DELETE)

        twitter/ (GET|POST|DELETE)
            <id>/ (GET|PUT|DELETE)

        facebook/ (GET|DELETE)
            <id>/ (GET|PUT|DELETE)

    me (GET)






