"""
Ticket Tracking System

This module implements a ticket management system for customer support teams.
It allows for tracking support tickets, managing queues, prioritizing issues,
and filtering tickets based on various criteria.

Each ticket has the following attributes:
- id: Unique identifier for the ticket
- title: Brief description of the issue
- type: Category of the ticket (technical, billing, general, account, feature)
- priority: Importance level (1-4, where 1 is highest priority)
- status: Current state of the ticket (new, open, resolved, closed)
"""

def initialize_data():
    """
    Initialize the system with predefined ticket data.
    
    Returns:
        tuple: Contains three elements:
            - List of regular tickets
            - List of escalated tickets
            - Empty list for active queue
    """
    tickets = [
        {"id": "T001", "title": "Payment not processing", "type": "billing", "priority": 2, "status": "open"},
        {"id": "T002", "title": "Reset password", "type": "account", "priority": 3, "status": "new"},
        {"id": "T003", "title": "Application crashes", "type": "technical", "priority": 1, "status": "open"},
        {"id": "T004", "title": "Add dark mode", "type": "feature", "priority": 4, "status": "new"},
        {"id": "T005", "title": "Renewal failed", "type": "billing", "priority": 2, "status": "open"}
    ]
    
    escalated = [
        {"id": "E001", "title": "Security breach", "type": "technical", "priority": 1, "status": "new"},
        {"id": "E002", "title": "Double-charged", "type": "billing", "priority": 1, "status": "new"}
    ]
    
    return tickets, escalated, []

def add_ticket(tickets, ticket):
    """
    Add a new ticket to the ticket list.
    
    Args:
        tickets (list): The current list of tickets
        ticket (dict): The new ticket to add
    
    Returns:
        list: Updated list of tickets
    
    Raises:
        ValueError: If ticket is missing required fields or has invalid values
    """
    # Validate ticket structure
    required_fields = ["id", "title", "type", "priority", "status"]
    for field in required_fields:
        if field not in ticket:
            raise ValueError(f"Ticket is missing required field: {field}")
    
    # Validate ticket type
    valid_types = ["technical", "billing", "general", "account", "feature"]
    if ticket["type"] not in valid_types:
        raise ValueError(f"Invalid ticket type. Must be one of: {', '.join(valid_types)}")
    
    # Validate priority (1-4)
    if not isinstance(ticket["priority"], int) or ticket["priority"] < 1 or ticket["priority"] > 4:
        raise ValueError("Priority must be an integer between 1 and 4")
    
    # Validate status
    valid_statuses = ["new", "open", "resolved", "closed"]
    if ticket["status"] not in valid_statuses:
        raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
    
    # Add the ticket to the list
    tickets.append(ticket)
    return tickets

def remove_ticket(tickets, index):
    """
    Remove a ticket from the ticket list.
    
    Args:
        tickets (list): The current list of tickets
        index (int): The index of the ticket to remove
    
    Returns:
        dict: The removed ticket
    
    Raises:
        IndexError: If the index is out of range
    """
    if index < 0 or index >= len(tickets):
        raise IndexError("Index out of range")
    
    return tickets.pop(index)

def sort_tickets(tickets, key):
    """
    Sort tickets based on a specified key.
    
    Args:
        tickets (list): The list of tickets to sort
        key (str): The key to sort by (id, priority, status, type)
    
    Returns:
        list: Sorted list of tickets
    
    Raises:
        ValueError: If the key is invalid
    """
    valid_keys = ["id", "priority", "status", "type"]
    if key not in valid_keys:
        raise ValueError(f"Invalid sort key. Must be one of: {', '.join(valid_keys)}")
    
    # Make a copy to avoid modifying the original list
    sorted_tickets = tickets.copy()
    
    # Sort by the specified key
    sorted_tickets.sort(key=lambda ticket: ticket[key])
    
    return sorted_tickets

def filter_tickets(tickets, filter_type, value):
    """
    Filter tickets based on specified criteria.
    
    Args:
        tickets (list): The list of tickets to filter
        filter_type (str): The type of filter to apply (type, status, priority, keyword)
        value: The value to filter by
    
    Returns:
        list: Filtered list of tickets
    
    Raises:
        ValueError: If the filter type is invalid
    """
    valid_filters = ["type", "status", "priority", "keyword"]
    if filter_type not in valid_filters:
        raise ValueError(f"Invalid filter type. Must be one of: {', '.join(valid_filters)}")
    
    if filter_type == "keyword":
        # Search for keyword in title using list comprehension
        value = value.lower()
        return [ticket for ticket in tickets if value in ticket["title"].lower()]
    elif filter_type == "priority":
        # Convert value to int if it's a string
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                raise ValueError("Priority value must be a number between 1 and 4")
        
        # Filter by priority using list comprehension
        return [ticket for ticket in tickets if ticket["priority"] == value]
    else:
        # Filter by type or status using list comprehension
        return [ticket for ticket in tickets if ticket[filter_type] == value]

def combine_queues(tickets1, tickets2):
    """
    Combine two ticket queues into a single list.
    
    Args:
        tickets1 (list): First list of tickets
        tickets2 (list): Second list of tickets
    
    Returns:
        list: Combined list of tickets
    """
    # Create a new list with all tickets from both lists using the + operator
    return tickets1 + tickets2

def get_priority_tickets(tickets, priority_level):
    """
    Get tickets with a specific priority level.
    
    Args:
        tickets (list): The list of tickets
        priority_level (int): The priority level to filter by (1-4)
    
    Returns:
        list: List of tickets with the specified priority
    
    Raises:
        ValueError: If priority level is invalid
    """
    if not isinstance(priority_level, int) or priority_level < 1 or priority_level > 4:
        raise ValueError("Priority level must be between 1 and 4")
    
    # Use list comprehension to filter by priority
    return [ticket for ticket in tickets if ticket["priority"] == priority_level]

def manage_queue(tickets, active_queue, operation, index=None):
    """
    Manage the active queue of tickets being worked on.
    
    Args:
        tickets (list): The master list of tickets
        active_queue (list): The current active queue
        operation (str): The operation to perform (add, remove, clear)
        index (int, optional): The index for add/remove operations
    
    Returns:
        list: The updated active queue
    
    Raises:
        ValueError: If operation is invalid or queue exceeds capacity
        IndexError: If index is out of range
    """
    valid_operations = ["add", "remove", "clear"]
    if operation not in valid_operations:
        raise ValueError(f"Invalid operation. Must be one of: {', '.join(valid_operations)}")
    
    if operation == "add":
        if index is None:
            raise ValueError("Index is required for add operation")
        
        if index < 0 or index >= len(tickets):
            raise IndexError("Ticket index out of range")
        
        # Check queue capacity (maximum 5 tickets)
        if len(active_queue) >= 5:
            raise ValueError("Active queue is at maximum capacity (5 tickets)")
        
        active_queue.append(tickets[index])
    
    elif operation == "remove":
        if index is None:
            raise ValueError("Index is required for remove operation")
        
        if index < 0 or index >= len(active_queue):
            raise IndexError("Queue index out of range")
        
        return active_queue.pop(index)
    
    elif operation == "clear":
        active_queue.clear()
    
    return active_queue

def update_ticket(tickets, index, field, value):
    """
    Update a specific field of a ticket.
    
    Args:
        tickets (list): The list of tickets
        index (int): The index of the ticket to update
        field (str): The field to update (status, priority, type)
        value: The new value for the field
    
    Returns:
        dict: The updated ticket
    
    Raises:
        IndexError: If the index is out of range
        ValueError: If the field or value is invalid
    """
    if index < 0 or index >= len(tickets):
        raise IndexError("Ticket index out of range")
    
    valid_fields = ["status", "priority", "type"]
    if field not in valid_fields:
        raise ValueError(f"Invalid field. Must be one of: {', '.join(valid_fields)}")
    
    ticket = tickets[index]
    
    if field == "status":
        valid_statuses = ["new", "open", "resolved", "closed"]
        if value not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        ticket["status"] = value
    
    elif field == "priority":
        try:
            priority = int(value)
            if priority < 1 or priority > 4:
                raise ValueError()
        except ValueError:
            raise ValueError("Priority must be an integer between 1 and 4")
        ticket["priority"] = priority
    
    elif field == "type":
        valid_types = ["technical", "billing", "general", "account", "feature"]
        if value not in valid_types:
            raise ValueError(f"Invalid type. Must be one of: {', '.join(valid_types)}")
        ticket["type"] = value
    
    return ticket

def get_formatted_ticket(ticket):
    """
    Format a ticket for display.
    
    Args:
        ticket (dict): The ticket to format
    
    Returns:
        str: Formatted ticket string
    """
    # Get priority level text
    priority_indicators = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    priority_text = priority_indicators[ticket["priority"] - 1]
    
    # Get status indicator
    status_text = ticket["status"].upper()
    
    return f"{ticket['id']} | {ticket['title']} | {ticket['type']} | Priority: {priority_text} ({ticket['priority']}) | Status: {status_text}"

def display_data(data, data_type="tickets"):
    """
    Display ticket data or queue.
    
    Args:
        data (list): The data to display
        data_type (str): The type of data (tickets, queue, filtered)
    """
    if not data:
        print("No tickets to display.")
        return
    
    if data_type == "tickets":
        print("Current Ticket List:")
    elif data_type == "queue":
        print("Active Queue:")
    elif data_type == "filtered":
        print("Filtered Results:")
    
    for ticket in data:
        print(get_formatted_ticket(ticket))

def main():
    """
    Main program function.
    """
    tickets, escalated, active_queue = initialize_data()
    
    # Display welcome message
    print("===== TICKET TRACKING SYSTEM =====")
    print(f"Total Tickets: {len(tickets)}")
    
    # Display critical tickets
    critical_tickets = get_priority_tickets(tickets, 1)
    print(f"Critical Tickets: {len(critical_tickets)}")
    
    running = True
    while running:
        print("\nMenu Options:")
        print("1. View Tickets")
        print("2. Add/Remove Ticket")
        print("3. Sort Tickets")
        print("4. Filter Tickets")
        print("5. Queue Operations")
        print("6. Process Escalated")
        print("7. Update Ticket")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # View tickets
            display_data(tickets)
        
        elif choice == "2":
            # Add/Remove ticket
            op = input("Enter 'add' or 'remove': ").lower()
            
            if op == "add":
                # Get ticket details
                id = input("Enter ticket ID: ")
                title = input("Enter title: ")
                ticket_type = input("Enter type (technical, billing, general, account, feature): ")
                priority = int(input("Enter priority (1-4): "))
                status = input("Enter status (new, open, resolved, closed): ")
                
                # Create ticket
                new_ticket = {
                    "id": id,
                    "title": title,
                    "type": ticket_type,
                    "priority": priority,
                    "status": status
                }
                
                try:
                    add_ticket(tickets, new_ticket)
                    print("Ticket added successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif op == "remove":
                # Display tickets with indices
                for i, ticket in enumerate(tickets):
                    print(f"{i}: {ticket['id']} - {ticket['title']}")
                
                index = int(input("Enter index to remove: "))
                
                try:
                    removed = remove_ticket(tickets, index)
                    print(f"Removed ticket: {removed['id']} - {removed['title']}")
                except IndexError:
                    print("Error: Invalid index.")
        
        elif choice == "3":
            # Sort tickets
            key = input("Sort by (id, priority, status, type): ")
            
            try:
                sorted_tickets = sort_tickets(tickets, key)
                display_data(sorted_tickets)
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            # Filter tickets
            filter_type = input("Filter by (type, status, priority, keyword): ")
            value = input("Enter value: ")
            
            try:
                filtered = filter_tickets(tickets, filter_type, value)
                display_data(filtered, "filtered")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "5":
            # Queue operations
            print("Active Queue Operations:")
            print("1. Add ticket to queue")
            print("2. Remove ticket from queue")
            print("3. View queue")
            print("4. Clear queue")
            
            queue_op = input("Enter choice: ")
            
            if queue_op == "1":
                # Display tickets with indices
                for i, ticket in enumerate(tickets):
                    print(f"{i}: {ticket['id']} - {ticket['title']}")
                
                index = int(input("Enter index to add: "))
                
                try:
                    manage_queue(tickets, active_queue, "add", index)
                    print("Ticket added to queue.")
                except (ValueError, IndexError) as e:
                    print(f"Error: {e}")
            
            elif queue_op == "2":
                # Display queue with indices
                for i, ticket in enumerate(active_queue):
                    print(f"{i}: {ticket['id']} - {ticket['title']}")
                
                if not active_queue:
                    print("Queue is empty.")
                    continue
                
                index = int(input("Enter index to remove: "))
                
                try:
                    removed = manage_queue(tickets, active_queue, "remove", index)
                    print(f"Removed from queue: {removed['id']} - {removed['title']}")
                except IndexError:
                    print("Error: Invalid index.")
            
            elif queue_op == "3":
                # View queue
                display_data(active_queue, "queue")
            
            elif queue_op == "4":
                # Clear queue
                manage_queue(tickets, active_queue, "clear")
                print("Queue cleared.")
        
        elif choice == "6":
            # Process escalated tickets
            print(f"Processing {len(escalated)} escalated tickets...")
            combined = combine_queues(tickets, escalated)
            print(f"Combined ticket count: {len(combined)}")
            
            # Display combined tickets
            display_data(combined)
            
            # Update tickets to include escalated
            confirm = input("Update main ticket list to include escalated? (y/n): ")
            if confirm.lower() == "y":
                tickets = combined
                escalated = []
                print("Main ticket list updated.")
        
        elif choice == "7":
            # Update ticket
            # Display tickets with indices
            for i, ticket in enumerate(tickets):
                print(f"{i}: {ticket['id']} - {ticket['title']}")
            
            index = int(input("Enter index to update: "))
            field = input("Enter field to update (status, priority, type): ")
            value = input("Enter new value: ")
            
            try:
                updated = update_ticket(tickets, index, field, value)
                print(f"Updated ticket: {updated['id']} - {updated['title']}")
                print(get_formatted_ticket(updated))
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
        
        elif choice == "0":
            # Exit
            print("Exiting system. Goodbye!")
            running = False
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()