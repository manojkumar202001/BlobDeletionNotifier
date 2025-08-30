const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

module.exports = async function (context, eventGridEvent) {
    const blobName = eventGridEvent.data.url.split('/').pop();
    context.log(`Blob deleted: ${blobName}`);

    const msg = {
        to: 'admin@example.com',
        from: 'noreply@example.com',
        subject: 'Blob Deleted Notification',
        text: `The blob ${blobName} was deleted.`,
    };

    try {
        await sgMail.send(msg);
        context.log('Email sent successfully');
    } catch (error) {
        context.log.error(error);
    }
};
