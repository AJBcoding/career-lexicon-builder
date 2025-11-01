-- Convert .pages files to PDF using Pages app
-- Usage: osascript convert_pages_to_pdf.applescript

set sourceFolder to (path to home folder as text) & "PycharmProjects:career-lexicon-builder:my_documents:"
set outputFolder to (path to home folder as text) & "PycharmProjects:career-lexicon-builder:my_documents:converted:"

-- Create output folder if it doesn't exist
tell application "Finder"
	if not (exists folder outputFolder) then
		make new folder at folder ((path to home folder as text) & "PycharmProjects:career-lexicon-builder:my_documents:") with properties {name:"converted"}
	end if
end tell

-- Get list of .pages files
tell application "Finder"
	set pagesFiles to every file of folder sourceFolder whose name extension is "pages"
end tell

-- Log start
log "Found " & (count of pagesFiles) & " .pages files to convert"

-- Convert each file
repeat with aFile in pagesFiles
	try
		set fileName to name of aFile
		set baseName to text 1 thru -7 of fileName -- Remove ".pages" extension
		set outputPath to outputFolder & baseName & ".pdf"

		-- Check if PDF already exists
		tell application "Finder"
			if exists file outputPath then
				log "⏭️  Skipping " & fileName & " (PDF already exists)"
			else
				log "🔄 Converting " & fileName & "..."

				-- Open file in Pages
				tell application "Pages"
					activate
					open (aFile as alias)
					delay 1 -- Wait for file to open

					-- Export as PDF
					set docName to name of front document
					export front document to file outputPath as PDF
					delay 0.5 -- Wait for export to complete

					-- Close without saving
					close front document saving no
				end tell

				log "✅ Converted " & fileName & " → " & baseName & ".pdf"
			end if
		end tell

	on error errMsg
		log "❌ Error converting " & fileName & ": " & errMsg
	end try
end repeat

-- Quit Pages
tell application "Pages"
	quit
end tell

log "✅ Conversion complete! PDFs saved to my_documents/converted/"
