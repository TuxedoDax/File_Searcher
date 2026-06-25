function WorkingDirectory
{

  #  Getting current directory
  $directory = Get-Location
  #  Creating a variable that we can more easily use to point to the required file.
  $directoryPath = $directory.Path + "\"

  return $directoryPath

}

function CSVImport ($directoryPath, $csvName)
{

  #  Creating the full path to the file we want to read, including the name.
  $csvPath = $directoryPath + $csvName
  #  Importing the file and saving it's content to a variable. (Currently only looking at a comma to delimit, this should be changed later.)
  $csvIle = Import-Csv $csvPath -Delimiter ","

  return $csvFile

}

function CSVReader ($csvFile, $headerName)
{

  $csvList = @()
  #  Reading the CSV and adding the specified $headerName to a variable we can return.
  foreach ($entry in $csvFile)
  {

    $csvList += $entry.$headerName

  }

  return $csvList

}

function ListCompare ($firstCSVName, $secondCSVName, $firstList, $secondList)
{

  #  List of comparisons we can currently provide with this script.
  Write-Host "Which option do you want to use?: `n
  Only itmes seen in $firstCSVName ? (1) `n
  Only items seen in $secondCSVName ? (2) `n
  Items seen in both lists. (3)"

  #  Obtaining compare requirement from user.
  $compareSwitch = Read-Host "Please select the option you wish to use"


  $results = @()
  $outputList = @()

  switch ($compareSwitch)
  {

    "1" { 
    Write-Host "Selection: Only items in $firstCSVName ."
    $results = Compare-Object $firstList $secondList | Where-Object {$_.SideIndicator -eq "<="}
    }

    "2" { 
    Write-Host "Selection: Only items in $secondCSVName ."
    $results = Compare-Object $firstList $secondList | Where-Object {$_.SideIndicator -eq "=>"}
    }

    "3" {
    Write-Host "Selection: Items in both CSV lists."
    $results = Compare-Object $firstList $secondList -IncludeEqual -ExcludeDifferent
    }
    
  }

  foreach ($entry in $results)
  {

    $resultsObject = $entry.InputObject
    $outputList += $resultObject

  }

  return $outputList

}

function ExportFile ($directoryPath, $outputList)
{

  #  Getting the current date and time for the export file.
  $currentTime = Get-Date -Format "MM-dd-yyyy-HHmm"

  #  File path for export.
  $exportPath = $directoryPath + "CSVCompareExport" + "_" + $currentTime + ".csv"

  #  Exporting the data to a file.
  $outputList | Out-File -FilePath $exportPath 

}

#  Getting the current working directory.
$directoryPath = WorkingDirectory

#  Name of the first file.
$firstCSVName = Read-Host "What is the name of your first file? (include '.csv')"

# Name of the second file.
$secondCSVName = Read-Host "What is the name of your first file? (include '.csv')"

#  Import First CSV
$firstFile = CSVImport $directoryPath $firstCSVName

#  Import Second CSV
$secondFile = CSVImport $directoryPath $secondCSVName

#  Getting the name of the column we wnat to read in.
$headerName = Read-Host "What is the name of the column, which appears in bnoth files, that we want to compare?"

#  Read the firstFile and store the column data specified in $headerName .
$firstList = CSVReader $firstFile $headerName

#  Read the secondFile and store the column data specified in $headerName .
$secondList = CSVReader $secondFile $headerName

#  Running the comparison.
$outputList = ListCompare $firstCSVName $secondCSVName $firstFile $secondList

#  Exporting the output that the script has detected.
ExportFile $directoryPath $outputList
