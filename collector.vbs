Option Explicit

Dim objWMIService, objProcess, colProcess, wshShell, strComputerName
Dim strComputer, strList, colStartupCommands, objStartupCommand, objFSO
Dim objFile, strNameOfUser, strUserDomain, colProperties


function md5hashBytes(aBytes)
    Dim MD5
    set MD5 = CreateObject("System.Security.Cryptography.MD5CryptoServiceProvider")

    MD5.Initialize()
    'Note you MUST use computehash_2 to get the correct version of this method, and the bytes MUST be double wrapped in brackets to ensure they get passed in correctly.
    md5hashBytes = MD5.ComputeHash_2( (aBytes) )
end function

function sha1hashBytes(aBytes)
    Dim sha1
    set sha1 = CreateObject("System.Security.Cryptography.SHA1Managed")

    sha1.Initialize()
    'Note you MUST use computehash_2 to get the correct version of this method, and the bytes MUST be double wrapped in brackets to ensure they get passed in correctly.
    sha1hashBytes = sha1.ComputeHash_2( (aBytes) )
end function

function sha256hashBytes(aBytes)
    Dim sha256
    set sha256 = CreateObject("System.Security.Cryptography.SHA256Managed")

    sha256.Initialize()
    'Note you MUST use computehash_2 to get the correct version of this method, and the bytes MUST be double wrapped in brackets to ensure they get passed in correctly.
    sha256hashBytes = sha256.ComputeHash_2( (aBytes) )
end function

function sha256HMACBytes(aBytes, aKey)
    Dim sha256
    set sha256 = CreateObject("System.Security.Cryptography.HMACSHA256")

    sha256.Initialize()
    sha256.key=aKey
    'Note you MUST use computehash_2 to get the correct version of this method, and the bytes MUST be double wrapped in brackets to ensure they get passed in correctly.
    sha256HMACBytes = sha256.ComputeHash_2( (aBytes) )
end function

function stringToUTFBytes(aString)
    Dim UTF8
    Set UTF8 = CreateObject("System.Text.UTF8Encoding")
    stringToUTFBytes = UTF8.GetBytes_4(aString)
end function

function bytesToHex(aBytes)
    dim hexStr, x
    for x=1 to lenb(aBytes)
        hexStr= hex(ascb(midb( (aBytes),x,1)))
        if len(hexStr)=1 then hexStr="0" & hexStr
        bytesToHex=bytesToHex & hexStr
    next
end function

Function BytesToBase64(varBytes)
    With CreateObject("MSXML2.DomDocument").CreateElement("b64")
        .dataType = "bin.base64"
        .nodeTypedValue = varBytes
        BytesToBase64 = .Text
    End With
End Function

'Special version that produces the URLEncoded variant of Base64 used in JWTs.
Function BytesToBase64UrlEncode(varBytes)
    With CreateObject("MSXML2.DomDocument").CreateElement("b64")
        .dataType = "bin.base64"
        .nodeTypedValue = varBytes
        BytesToBase64UrlEncode = replace(replace(replace(replace(replace(.Text,chr(13),""),chr(10),""),"+", "-"),"/", "_"),"=", "")
    End With
End Function

Function GetBytes(sPath)
    With CreateObject("Adodb.Stream")
        .Type = 1 ' adTypeBinary
        .Open
        .LoadFromFile sPath
        .Position = 0
        GetBytes = .Read
        .Close
    End With
End Function



Function GetConnections()
  Dim i, shExec, sh
  set sh = CreateObject("Wscript.Shell")
  Set objFSO = CreateObject("Scripting.FileSystemObject")
  Set objFile = objFSO.CreateTextFile(strComputerName & "_netstat.csv", True)
  i = 0
  set shExec = sh.Exec("netstat -an")
    Do While Not shExec.StdOut.AtEndOfStream
      objFile.Write shExec.StdOut.ReadLine() & vbCrLf
  Loop
End Function

Function GetRunningProcs()
    Set colProcess = objWMIService.ExecQuery ("Select * from Win32_Process")
    Set objFSO=CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.CreateTextFile(strComputerName&"_procs.csv", True)
    objFile.Write "ProcName, Command Line, User, ExePath, PPID, PID, Hash" & vbCrLf
    For Each objProcess in colProcess
        Dim ProcName
        ProcName = objProcess.ExecutablePath
        If IsNull(ProcName) Or IsEmpty(ProcName) Then
            strList = objProcess.Name & ", " & objProcess.CommandLine & ", " & strUserDomain &"/"& strNameOfUser & _
            ", " & objProcess.ExecutablePath & ", " & objProcess.ParentProcessId & ", " & objProcess.ProcessId & _
            ", *" & vbCrLf
        Else
            Err.Clear
            ProcName = "*"
            On Error Resume Next
                ProcName = bytesToHex(sha256hashBytes(GetBytes(objProcess.ExecutablePath)))
            On Error GoTo 0
            strList = objProcess.Name & ", " & objProcess.CommandLine & ", " & strUserDomain &"/"& strNameOfUser & _
            ", " & objProcess.ExecutablePath & ", " & objProcess.ParentProcessId & ", " & objProcess.ProcessId & _
            ", " & ProcName & vbCrLf
        End If
      objFile.Write strList
      WScript.Echo "Wrote: " & strList
      'On Error Resume Next
      Next
    objFile.Close
End Function

Function GetStartupProcs()
    Set colStartupCommands = objWMIService.ExecQuery ("Select * from Win32_StartupCommand")
    Set objFSO=CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.CreateTextFile(strComputerName&"_startups.csv", True)
    objFile.Write "Command, Desc, Location, Name, User" & vbCrLf
    For Each objStartupCommand in colStartupCommands
        strList = "" & _
        objStartupCommand.Command & ", " & _
        objStartupCommand.Description & ", " & _
        objStartupCommand.Location & ", " & _
        objStartupCommand.Name & ", " & _
        objStartupCommand.User & vbCrLf
        objFile.Write strList
    Next
    objFile.Close
End Function


Err.Clear
strComputer = "."

Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
Set wshShell = CreateObject( "WScript.Shell" )
strComputerName = wshShell.ExpandEnvironmentStrings( "%COMPUTERNAME%" )

''' Start Actual Aquisition '''
call GetRunningProcs()
call GetStartupProcs()
call GetConnections()

WScript.Quit
