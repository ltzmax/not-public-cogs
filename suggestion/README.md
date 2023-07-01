# Suggestion Help

Customizable suggestion cog to various purposes.

# sendmsg
 - Usage: `[p]send <message> `
 - Aliases: `sendmessage and sendmsg`
 - Checks: `server_only`

Send your message to the set channel.<br/><br/>**Example:**<br/>`[p]send This is my suggestion!` - This will send your message to the set channel.

# suggestionset
 - Usage: `[p]suggestionset `
 - Restricted to: `ADMIN`
 - Aliases: `suggestset and setsuggest`
 - Checks: `server_only`

Manage suggestion settings.

## suggestionset view
 - Usage: `[p]suggestionset view `

View the current settings.

## suggestionset title
 - Usage: `[p]suggestionset title [title] `

Set or reset the title.<br/><br/>This is the title of the embed where it's currently set to "Suggestion".<br/>If no title is provided, it will reset the title.<br/>The title must be 256 characters or less.<br/><br/>**Example:**<br/>`[p]suggestionset title My Suggestion` - This will set the title to "My Suggestion".<br/>`[p]suggestionset title` - This will reset the title to "Suggestion".

## suggestionset version
 - Usage: `[p]suggestionset version `

Shows the version of the cog.

## suggestionset buttons
 - Usage: `[p]suggestionset buttons [toggle=None] `
 - Aliases: `react`

Toggle whether to up/down vote.<br/><br/>It is disabled by default.<br/>If no toggle is provided, it will toggle the current setting.

## suggestionset channel
 - Usage: `[p]suggestionset channel [channel=None] `

Set or clear the channel.<br/><br/>If no channel is provided, it will clear the channel.<br/><br/>**Example:**<br/>`[p]suggestionset channel #suggestions` - This will set the channel to #suggestions.<br/>`[p]suggestionset channel` - This will clear the channel.
