//-----------------------------------------------------------------------------
//
//	CentralScene.h
//
//	Implementation of the Z-Wave COMMAND_CLASS_CENTRAL_SCENE
//
//	Copyright (c) 2012 Greg Satz <satz@iranger.com>
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

#ifndef _SoundSwitch_H
#define _SoundSwitch_H

#include "command_classes/CommandClass.h"

namespace OpenZWave
{
	class ValueByte;

	/** \brief Implements COMMAND_CLASS_SOUND_SWITCH (0x79), a Z-Wave device command class.
	 */
	class SoundSwitch: public CommandClass
	{
	public:
		static CommandClass* Create( uint32 const _homeId, uint8 const _nodeId ){ return new SoundSwitch( _homeId, _nodeId ); }
		virtual ~SoundSwitch(){}
		static uint8 const StaticGetCommandClassId(){ return 0x79; }
		static string const StaticGetCommandClassName(){ return "COMMAND_CLASS_SOUND_SWITCH"; }

		// From CommandClass
		virtual uint8 const GetCommandClassId()const{ return StaticGetCommandClassId(); }
		virtual string const GetCommandClassName()const{ return StaticGetCommandClassName(); }
		virtual uint8 GetMaxVersion(){ return 1; }
		virtual bool HandleMsg( uint8 const* _data, uint32 const _length, uint32 const _instance = 1 );
		virtual bool SetValue( Value const& _value );
		
		void ReadXML( TiXmlElement const* _ccElement	);
		void WriteXML( TiXmlElement* _ccElement );
		virtual bool RequestState( uint32 const _requestFlags, uint8 const _instance, Driver::MsgQueue const _queue );
		virtual bool RequestValue( uint32 const _requestFlags, uint8 const _what, uint8 const _instance, Driver::MsgQueue const _queue );
	protected:
		virtual void CreateVars( uint8 const _instance );
	private:
		SoundSwitch( uint32 const _homeId, uint8 const _nodeId );
		int32 m_tonecount;
	};

} // namespace OpenZWave

#endif
