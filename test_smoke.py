def test_imports():
    try:
        import chat_backend
        import tools
        import agent_tools.animal_utils
        import agent_tools.profile_tools
    except Exception as e:
        assert False, f"Import failed: {e}"

def test_send_message_returns_reply():
    from chat_backend import send_message
    reply = send_message("Ahoj, já jsem Lucka a mám ráda žirafy!")
    print("Odpověď:", reply)
    assert isinstance(reply, str) and len(reply) > 0, "Odpověď od asistenta je neplatná."

def test_extract_profile_via_gpt():
    from agent_tools.profile_tools import extract_profile_via_gpt, session_profile
    extract_profile_via_gpt("Ahoj, já jsem Ondra, je mi 6 let a mám rád tučňáky.")
    assert all(k in session_profile and session_profile[k] for k in ["jméno", "věk", "zvíře"]), "Profil nebyl správně extrahován."
