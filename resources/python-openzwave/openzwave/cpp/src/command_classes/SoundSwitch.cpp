//-----------------------------------------------------------------------------
//
//	Color.cpp
//
//	Implementation of the Z-Wave COMMAND_CLASS_COLOR
//
//	Copyright (c) 2014 GizMoCuz
//
//	SOFTWARE NOTICE AND LICENSE
//
//	This file is part of OpenZWave.
//
//	OpenZWave is free software: you can redistribute it and/or modify
//	it under the terms of the GNU Lesser General Public License as published
//	by the Free Software Foundation, either version 3 of the License,
//	or (at your option) any later version.
//
//	OpenZWave is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU Lesser General Public License for more details.
//
//	You should have received a copy of the GNU Lesser General Public License
//	along with OpenZWave.  If not, see <http://www.gnu.org/licenses/>.
//
//-----------------------------------------------------------------------------

#include <iostream>
#include <iomanip>


#include "command_classes/CommandClasses.h"
#include "command_classes/SoundSwitch.h"
#include "Defs.h"
#include "Msg.h"
#include "Node.h"
#include "Driver.h"
#include "platform/Log.h"

#include "value_classes/ValueInt.h"
#include "value_classes/ValueString.h"
#include "value_classes/ValueByte.h"

#include "tinyxml.h"


using namespace OpenZWave;

enum SoundSwitchCmd
{
	SoundSwitch_ToneNum_Get = 0x01,
	SoundSwitch_ToneNum_Report = 0x02,
	SoundSwitch_ToneInfo_Get = 0x03,
	SoundSwitch_ToneInfo_Report = 0x04,
	SoundSwitch_Config_Set = 0x05,
	SoundSwitch_Config_Get = 0x06,
	SoundSwitch_Config_Report = 0x07,
	SoundSwitch_Play_Set = 0x08,
	SoundSwitch_Play_Get = 0x09,
	SoundSwitch_Play_Report = 0x0A
};
//-----------------------------------------------------------------------------
// <SoundSwitch::SoundSwitch>
// Constructor
//-----------------------------------------------------------------------------
SoundSwitch::SoundSwitch
(
		uint32 const _homeId,
		uint8 const _nodeId
):
CommandClass( _homeId, _nodeId ),
m_tonecount(0)
{
    SetStaticRequest( StaticRequest_Values );
	Log::Write(LogLevel_Info, GetNodeId(), "SoundSwitch - Created %d", HasStaticRequest( StaticRequest_Values ));
}



//-----------------------------------------------------------------------------
// <SoundSwitch::RequestState>
// Request current state from the device
//-----------------------------------------------------------------------------
bool SoundSwitch::RequestState
(
		uint32 const _requestFlags,
		uint8 const _instance,
		Driver::MsgQueue const _queue
)
{
	bool res = false;
	if( _requestFlags & RequestFlag_Static )
		{
			Msg* msg = new Msg( "SoundSwitch_ToneNum_Get", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId() );
			msg->SetInstance( this, _instance );
			msg->Append( GetNodeId() );
			msg->Append( 2 );
			msg->Append( GetCommandClassId() );
			msg->Append( SoundSwitch_ToneNum_Get );
			msg->Append( GetDriver()->GetTransmitOptions() );
			GetDriver()->SendMsg( msg, _queue );
			res = true;
		}
	if( _requestFlags & RequestFlag_Dynamic )
	{
		res |= RequestValue( _requestFlags, 0, _instance, _queue );
	}
	return res;
}

//-----------------------------------------------------------------------------
// <SoundSwitch::RequestValue>
// Request current value from the device
//-----------------------------------------------------------------------------
bool SoundSwitch::RequestValue
(
		uint32 const _requestFlags,
		uint8 const _what,
		uint8 const _instance,
		Driver::MsgQueue const _queue
)
{
	if (_what == SoundSwitch_ToneNum_Get) {
		Msg* msg = new Msg( "SoundSwitch_ToneNum_Get", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId() );
		msg->SetInstance( this, _instance );
		msg->Append( GetNodeId() );
		msg->Append( 2 );
		msg->Append( GetCommandClassId() );
		msg->Append( _what );
		msg->Append( GetDriver()->GetTransmitOptions() );
		GetDriver()->SendMsg( msg, _queue );
	}
	return true;
}
//-----------------------------------------------------------------------------
// <SoundSwitch::ReadXML>
// Class specific configuration
//-----------------------------------------------------------------------------
void SoundSwitch::ReadXML
(
		TiXmlElement const* _ccElement
)
{
	int32 intVal;

	CommandClass::ReadXML( _ccElement );
	if( TIXML_SUCCESS == _ccElement->QueryIntAttribute( "tonecount", &intVal ) )
	{
		m_tonecount = intVal;
	}
}

//-----------------------------------------------------------------------------
// <SoundSwitch::WriteXML>
// Class specific configuration
//-----------------------------------------------------------------------------
void SoundSwitch::WriteXML
(
		TiXmlElement* _ccElement
)
{
	char str[32];

	CommandClass::WriteXML( _ccElement );
	snprintf( str, sizeof(str), "%d", m_tonecount );
	_ccElement->SetAttribute( "tonecount", str);
}


//-----------------------------------------------------------------------------
// <SoundSwitch::HandleMsg>
// Handle a message from the Z-Wave network
//-----------------------------------------------------------------------------
bool SoundSwitch::HandleMsg
(
		uint8 const* _data,
		uint32 const _length,
		uint32 const _instance	// = 1
)
{
	if (SoundSwitch_ToneNum_Report == (SoundSwitchCmd)_data[0])
	{
		/* Create a Number of ValueID's based on the m_scenecount variable
		 * We prefer what the Config File specifies rather than what is returned by
		 * the Device...
		 */
		int tonecount = _data[1];
		if (m_tonecount == 0)
		{
			m_tonecount = tonecount;
		}
		if ( ValueInt* value = static_cast<ValueInt*>( GetValue( _instance, 0x00)))
		{
			value->OnValueRefreshed(m_tonecount);
			value->Release();
		} else {
			Log::Write( LogLevel_Warning, GetNodeId(), "Can't find ValueID for ToneCount");
		}
	}

	return false;
}

//-----------------------------------------------------------------------------
// <SoundSwitch::SetValue>
// Set a new value for the sound
//-----------------------------------------------------------------------------
bool SoundSwitch::SetValue
(
	Value const& _value
)
{
	uint8 instance = _value.GetID().GetInstance();

	switch( _value.GetID().GetIndex() )
	{
		case SoundSwitch_Play_Set:
		{
			ValueByte const* value = static_cast<ValueByte const*>(&_value);
			ValueByte* valueObj = static_cast<ValueByte*>( GetValue( instance, SoundSwitch_Play_Set ) );
			Log::Write( LogLevel_Info, GetNodeId(), "Play sound::Set - Setting node %d to %d", GetNodeId(), value->GetValue());
			Msg* msg = new Msg( "SoundPlay_Set", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true );
			msg->SetInstance( this, instance );
			msg->Append( GetNodeId() );
			msg->Append( 3 );
			msg->Append( GetCommandClassId() );
			msg->Append( SoundSwitch_Play_Set );
			msg->Append( value->GetValue() );
			msg->Append( GetDriver()->GetTransmitOptions() );
			GetDriver()->SendMsg( msg, Driver::MsgQueue_Send );
			valueObj->OnValueRefreshed(value->GetValue());
			valueObj->Release();
			return true;
			break;
		}
	}
	return false;
}

//-----------------------------------------------------------------------------
// <SoundSwitch::CreateVars>
// Create the values managed by this command class
//-----------------------------------------------------------------------------
void SoundSwitch::CreateVars
(
		uint8 const _instance
)
{
	if( Node* node = GetNodeUnsafe() )
	{
		node->CreateValueInt( ValueID::ValueGenre_User, GetCommandClassId(), _instance, 0x00, "Tone Count", "", true, false, 0, 0 );
		node->CreateValueByte( ValueID::ValueGenre_User, GetCommandClassId(), _instance, 0x08, "Play Tone", "", false, false, 0, 0 );
	}
}