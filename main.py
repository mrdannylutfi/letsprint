import psutil

def detect_printer_drive(target_label=""):
    """
    Scans mounted drives to find a printer or its SD card.
    Optionally filters by the volume label (e.g., "PRINTER", "ENDER").
    """
    # 1. Get all mounted disk partitions
    partitions = psutil.disk_partitions(all=False)
    
    for partition in partitions:
        # 2. Filter for removable drives (common for printers/SD cards)
        # 'removable' is highly reliable on Windows. On Linux/Mac, check mount paths.
        if 'removable' in partition.opts or partition.mountpoint.startswith(('/Volumes', '/media')):
            
            drive_letter = partition.mountpoint
            
            # 3. Optional: Check for a specific volume name/label
            if target_label:
                try:
                    # Windows specific label check; falls back on other OS
                    import win32api
                    volume_name = win32api.GetVolumeInformation(drive_letter)[0]
                    if target_label.lower() in volume_name.lower():
                        return drive_letter
                except ImportError:
                    # Generic fallback if win32api isn't installed
                    if target_label.lower() in drive_letter.lower():
                        return drive_letter
            else:
                # If no label is specified, return the first removable drive found
                return drive_letter
                
    return None

# Example usage
printer_path = detect_printer_drive()
if printer_path:
    print(f"Printer drive detected at: **{printer_path}**")
else:
    print("No printer drive detected.")
